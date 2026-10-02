"""
=============================================================================
MULTI-RUN CAMPAIGN ENTRY POINT (thin wrapper over run_phase1_research.py)
=============================================================================
run_phase1_research.py drives ONE run (one run_id) from its current
pending_stage to a terminal state or a human pause, then exits. This module
adds the missing layer on top: pull the next ready brief from
config/campaign_queue.yaml, launch it, follow its lineage through any
reframe/escalation the orchestrator's own routing produces, detect the run
reaching a terminal state, and either advance to the next queued brief or
halt the whole campaign on a hard-pause condition.

Through the K4 kernel (2026-07-13, see docs/design/K4_routing_registration_
design_20260712.md), workflow/run_phase1_research.py's routing functions
(_route_refine/_route_pivot/_route_escalate) now also write two small fields
(continuation_child, continuation_created_by) onto their OWN run's
pipeline_state.yaml, read back by process_once() below instead of a
runs/-directory diff. Before K4, nothing in that file was modified from this
wrapper's own work; this file still only READS its module-level helpers
(load_yaml, save_yaml, update_state, load_campaign_state, run_loop,
resume_pipeline) and the on-disk artifacts it already produces -- the K4
change lives entirely inside run_phase1_research.py itself, not here.

THE QUEUE (config/campaign_queue.yaml):
Ordered list of briefs. One entry = one research question. An entry's
`run_ids` list grows as the SAME brief's lineage continues across
reframe/escalation (completed_reframed / completed_escalated) — those are
NOT new queue items, they're the orchestrator's own within-brief routing.
Only a genuinely new terminal state (completed_promoted, completed_rejected,
completed_escalated-with-no-instruments-left, etc.) advances the queue to
the NEXT brief.

HARD PAUSE CONDITIONS (never routed around — the whole campaign halts):
  1. no_signal_artifact              (F5c engineering pause)
  2. conformance_gate_failure        (F4d pre-registration conformance gate)
  3. wishlist_trigger                (campaign_review recommends consuming a
                                       detector_wishlist.yaml / feed_wishlist.yaml
                                       entry via reframe or escalate_component —
                                       see _check_wishlist_trigger)
  4. provisional_promote_*           (holdout gate — awaiting holdout_result.yaml,
                                       or holdout_result.yaml is inconclusive)
  5. budget_breaker                  (per-run weighted token budget exceeded)
  + unhandled_exception              (run_loop's own except-block failure)
  + stage_exception                  (E-061 C1.4: an exception that ESCAPED
                                       run_loop -- classified here, never a
                                       crashed campaign process)
  + launch_exception                 (E-061 C1.4: an exception while launching,
                                       before run_loop -- the run dir, if any, is
                                       recorded and paused, never orphaned)
  + flag_misconfiguration /          (E-061 C1.5: the launch pre-flight, before
    protocol_promotion_unratified     any LLM call -- see _flag_preflight_refusal
                                       and _protocol_preflight_refusal)
  + a residual bucket for every other status=="paused_for_human" case
    (component_gap, new_component escalation, regime_misattribution,
    component_execution_error, data-block HITL, verdict-verification failure)
    — all of these ALREADY halt via the orchestrator's own status field; this
    wrapper just refuses to auto-advance past them, same as the five above.

See RUNBOOK.md for the operational playbook (launch / status / resume / stop).
=============================================================================
"""

import argparse
import contextlib
import copy
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import traceback
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import run_phase1_research as orch  # noqa: E402  (path insert must precede this)
import campaign_lock  # noqa: E402  (E-011 S1b, single-writer campaign launch lock)
import record_schema  # noqa: E402  (closed record schema, see _save_queue)
import verdict_criteria_evaluator as vce  # noqa: E402  (G6, see _save_queue)
import campaign_review_retired as crr  # noqa: E402  (slice 6c S2b: shared with the orchestrator)
import composition_names as _composition_names  # noqa: E402  (E-060 S3b: shared names)
import protocol_resolution  # noqa: E402  (E-061 C1.5: the D-3 guard, checked at launch)
import abandoned_launch  # noqa: E402  (E-061 C1.4: the abandoned-launch marker, one source)
from setup_run import setup_run  # noqa: E402
from timeframe import timeframe_seconds  # noqa: E402  (E-061 C1.7 second-round: shared bar-size arithmetic)

# CUL-213: this is the unattended campaign entry point; its emoji status prints
# crash on a Windows cp1252 console (UnicodeEncodeError) the moment stdout is
# redirected/piped/logged. Carry the guard directly rather than relying on the
# transitive import of run_phase1_research above — same fix as setup_run.py
# (CUL-12). getattr because typeshed types sys.stdout as TextIO (no reconfigure);
# contextlib.suppress because a captured stream may reject it (OSError).
_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    with contextlib.suppress(OSError):
        _reconfigure(errors="replace")

ROOT = Path(__file__).resolve().parent.parent
QUEUE_PATH = ROOT / "config" / "campaign_queue.yaml"
CAMPAIGN_LOG_PATH = ROOT / "campaign_record" / "campaign_log.md"
CAMPAIGN_SUMMARY_PATH = ROOT / "campaign_record" / "campaign_summary.md"
# A3 (K4 kernel): frozen baseline of run directories that predate or fall
# outside the normal atomic registration path -- see
# engineering/improvements/done/design_and_docs/K4_routing_registration_design_20260712.md section 6.
BASELINE_PATH = ROOT / "config" / "campaign_baseline_runs.yaml"

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)

# Terminal pending_stage values that mean "this brief's lineage is truly done"
# (as opposed to completed_reframed/completed_escalated, which spawn a
# continuation run under the SAME queue entry — see process_once()).
# completed_refined added 2026-07-13 (K4/A1) -- both _route_refine and
# _route_pivot return this same string (A2 is the separate, later ledger item
# that would give them distinct terminal strings; not done here).
_LINEAGE_CONTINUATION_STAGES = ("completed_reframed", "completed_escalated", "completed_refined")
# Slice 6c S2a: process_once's halt when a legacy continuation reaches it under
# orchestrator.verdict_routing_retired.enabled (RUNBOOK.md §3 row of this name).
LEGACY_CONTINUATION_HALT = "legacy_continuation_under_retired_routing"
# Slice 6c S2a code review (items 3, 5): the refinement_brief action is retired
# with the routing it fed, and a completed_<idea_status> run must cite its
# idea_status.yaml at DONE time (fail closed, never `ungated`).
REFINEMENT_BRIEF_HALT = "refinement_brief_under_retired_routing"
IDEA_STATUS_HALT = "idea_status_missing_at_done"
# Slice 6c S2b review fixes 3 + 5: a campaign-review reframe brief that cannot be
# registered at DONE (flag switched off, brief missing, id collision, refused
# registration) halts -- never a raw exception, never a silently dropped brief.
REFRAME_HALT = "campaign_review_reframe_unregistered"
# The legacy routers that mint a continuation child (K4 A1's
# continuation_created_by values; _route_kill records one with no child).
_LEGACY_MINTING_ROUTERS = ("_route_refine", "_route_pivot", "_route_escalate")
# Slice 6c S2c: a parked entry's queue status, one per park kind (they match
# record_schema._QUEUE_STATUS_RE's `paused:.+`). --resume skips them; only
# --unpark restores one. Written only under orchestrator.verdict_routing_retired.
PARKED_STATUS_PREFIX = "paused:waiting_for_"
PARKED_STATUSES = tuple(f"{PARKED_STATUS_PREFIX}{k}" for k in orch.PARK_KINDS)
# E-061 C1.4 (DELIVERY_REVIEW.md A4): an exception that escapes run_loop is a
# classified pause (RUNBOOK.md §3 row of this name), never a crashed campaign
# process that a restart re-crashes. The same name is the run's flag.
STAGE_EXCEPTION_HALT = "stage_exception"
# E-061 C1.5 (A6, A8): the launch pre-flight's two refusals, before any LLM call.
# A flag refusal is config-level (no run flag; --resume re-checks the config);
# a protocol refusal is run-level (the run's flag of the same name).
FLAG_PREFLIGHT_HALT = "flag_misconfiguration"
PROTOCOL_PREFLIGHT_HALT = "protocol_promotion_unratified"
# E-061 C1.4 review fix 6: an exception while launching (setup_run / materialize /
# the brief context / the queued card), before run_loop.
LAUNCH_EXCEPTION_HALT = "launch_exception"
# The run-level halts above: each sets flags.<reason> on the run, cleared by a
# successful --resume (review fix 1).
_RUN_FLAG_HALTS = orch.RUN_HALT_FLAGS  # (STAGE_EXCEPTION_, PROTOCOL_PREFLIGHT_, LAUNCH_EXCEPTION_HALT)


# ---------------------------------------------------------------------------
# Queue I/O
# ---------------------------------------------------------------------------

def _load_queue() -> dict:
    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _save_queue(queue: dict):
    """R4 (K4 kernel, 2026-07-13): temp-file-then-os.replace in QUEUE_PATH's
    own directory -- see run_phase1_research.save_yaml's identical rationale.
    campaign_queue.yaml is the clearest concurrent-writer-risk file in this
    repo (RUNBOOK.md's single-writer-per-state-store rule names it
    explicitly), so a crash mid-write can no longer leave a truncated/partial
    queue file for the next reader.

    G6 / C7-EXT-R (D-4): every entry clears verdict-provenance BEFORE the file is
    written. The independent audit found this writer bypassed the gate entirely --
    `validate_verdict_provenance` had exactly one call site in the repository, on
    the KB side, so the queue's own `outcome` field (which is what
    `_regenerate_summary` and every human reader actually consult) could record a
    kill with nothing behind it. Validating the WHOLE list, not just the entry a
    caller happened to touch, is deliberate: it means a hand edit cannot ride into
    the file behind an unrelated legitimate write."""
    for entry in queue.get("queue") or []:
        if isinstance(entry, dict):
            # C7-EXT-R2: the QUEUE schema, not the KB one -- `status`, `priority`
            # and `relation` are legitimate here and meaningless there.
            vce.validate_verdict_provenance(
                entry, entry_ref=f"campaign_queue.yaml entry {entry.get('id')!r}",
                root=ROOT, schema=record_schema.QUEUE_ENTRY_SCHEMA)

    fd, tmp_name = tempfile.mkstemp(prefix=".campaign_queue.", suffix=".tmp",
                                     dir=str(QUEUE_PATH.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            yaml.safe_dump(queue, f, sort_keys=False, allow_unicode=True)
        os.replace(tmp_name, QUEUE_PATH)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _select_entry(entries: list) -> dict | None:
    """An entry already `in_progress` (its lineage isn't finished) always wins —
    this single-process wrapper only ever has one active lineage at a time.
    Otherwise, the highest-priority `ready` entry. `blocked_on_*` / `done` /
    `paused:*` entries are never auto-selected."""
    in_progress = [e for e in entries if e.get("status") == "in_progress"]
    if in_progress:
        return in_progress[0]
    ready = [e for e in entries if e.get("status") == "ready"]
    if not ready:
        return None
    ready.sort(key=lambda e: e.get("priority", 999))
    return ready[0]


def _next_action_for_entry(entry: dict) -> str:
    """B1/B2-non-regression (K4 kernel): the single classifier both
    process_once() and dry_run_verify() use to decide what happens next for
    a selected queue entry, so the two never diverge on what "the next
    action" means (see design note section 7 -- this does not achieve B2's
    full dry-run-parity fix, which also needs to simulate the plain
    "continue" branch; it only means B1's own new branch doesn't repeat
    B2's defect on day one).

    Returns "refinement_brief" (an unconsumed refinement_brief_path is
    present -- takes precedence over a plain continuation), "fresh_launch"
    (no run_ids yet), or "continue" (follow the existing lineage)."""
    if entry.get("refinement_brief_path") and \
       entry.get("refinement_brief_consumed_for") != entry["refinement_brief_path"]:
        return "refinement_brief"
    if not entry.get("run_ids"):
        # E-059 S2b (decision 9): a brief's extra card skips authoring -- it
        # launches past step 1a with its saved card. Only such entries carry
        # card_ref, so every other entry's action is unchanged.
        if entry.get("card_ref"):
            return "queued_card"
        return "fresh_launch"
    return "continue"


def _run_state(run_id: str) -> dict:
    path = ROOT / "runs" / run_id / "pipeline_state.yaml"
    return (orch.load_yaml(path) or {}) if path.exists() else {}


def _legacy_continuation_blocker(entry: dict) -> str | None:
    """Slice 6c S2a (code review item 2). Why the entry's current run
    (run_ids[-1]) belongs to a lineage the retired routing extended, or None:
      * an earlier run of the entry recorded it as its continuation_child
        (the legacy router minted it -- the realistic case: the queue already
        followed the child before the flag was switched on);
      * it ended at a continuation stage with a continuation_child of its own;
      * its own continuation_created_by names a minting legacy router.
    Read-only. Used before run_loop, after it, and by --resume."""
    run_ids = entry.get("run_ids") or []
    if not run_ids:
        return None
    cur = run_ids[-1]
    for prev in run_ids[:-1]:
        pst = _run_state(prev)
        if pst.get("continuation_child") == cur:
            return (f"{cur} was minted by legacy routing: {prev}'s continuation_child is {cur!r} "
                    f"(written by {pst.get('continuation_created_by')!r})")
    st = _run_state(cur)
    if (st.get("pending_stage") or "") in _LINEAGE_CONTINUATION_STAGES and st.get("continuation_child"):
        return (f"{cur} ended {st.get('pending_stage')} with continuation_child="
                f"{st.get('continuation_child')!r} (written by {st.get('continuation_created_by')!r})")
    if st.get("continuation_created_by") in _LEGACY_MINTING_ROUTERS:
        return f"{cur}'s continuation_created_by is the legacy router {st.get('continuation_created_by')!r}"
    return None


def _idea_status_blocker(run_id: str, pending: str) -> str | None:
    """Slice 6c S2a (code review item 5). A run ending completed_<status>
    under the flag must cite a readable idea_status.yaml whose idea_status is
    that same status; anything else is an integrity failure, returned as text."""
    ref = ROOT / "runs" / run_id / "artifacts" / "idea_status.yaml"
    expected = pending[len("completed_"):]
    if not ref.exists():
        return f"{run_id} ended {pending} but runs/{run_id}/artifacts/idea_status.yaml is missing"
    try:
        doc = orch.load_yaml(ref)
    except Exception as e:  # unreadable is the same integrity failure as missing
        return f"{run_id} ended {pending} but its idea_status.yaml is unreadable ({e})"
    status = doc.get("idea_status") if isinstance(doc, dict) else None
    if status != expected:
        return f"{run_id} ended {pending} but its idea_status.yaml reads idea_status={status!r}"
    return None


def _retired_routing_halt_blocker(entry: dict, reason: str) -> str | None:
    """For --resume: the condition behind one of this slice's halts, if it
    still holds (the run itself is not paused, so its status cannot say)."""
    if reason == LEGACY_CONTINUATION_HALT:
        return _legacy_continuation_blocker(entry)
    if reason == REFINEMENT_BRIEF_HALT:
        return ("the entry still carries an unconsumed refinement_brief_path"
                if _next_action_for_entry(entry) == "refinement_brief" else None)
    if reason == REFRAME_HALT and entry.get("run_ids"):
        run_id = entry["run_ids"][-1]
        return _reframe_registration_blocker(run_id, _run_state(run_id),
                                             orch._verdict_routing_retired_enabled())
    if reason == IDEA_STATUS_HALT and entry.get("run_ids"):
        run_id = entry["run_ids"][-1]
        pending = _run_state(run_id).get("pending_stage") or ""
        if pending in orch.RETIRED_ROUTING_TERMINALS:
            return _idea_status_blocker(run_id, pending)
    return None


def _halt_retired_routing(queue: dict, entry: dict, run_id, reason: str,
                          detail: str, schedulability_enabled: bool) -> bool:
    """One halt for this slice's process_once refusals: paused:<reason>, a
    halt_history record on the run (when there is one), a HALT log line."""
    entry["status"] = f"paused:{reason}"
    _save_queue(queue)
    _regenerate_summary(queue)
    if run_id and (ROOT / "runs" / run_id / "pipeline_state.yaml").exists():
        run_dir = ROOT / "runs" / run_id
        _append_halt_history(run_dir, orch.load_yaml(run_dir / "pipeline_state.yaml") or {},
                             reason, detail)
    _log(f"HALT — {reason}: {detail}. Campaign stopped on {entry['id']}"
         f"{' / ' + run_id if run_id else ''}. See RUNBOOK.md §3.")
    _write_loop_health()
    if schedulability_enabled:
        _write_schedulability()
    return False


# ---------------------------------------------------------------------------
# Brief materialization
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Phase 1.3 (docs/CAMPAIGN_PROGRAM.md): venue/market_type registration-rule mechanism.
# Single source of truth: config/venue_tradability.yaml. Consumed by
# _materialize_run() below to auto-flag research_only on any brief whose
# declared venue+market_type isn't tradable==true, or whose venue/market_type is
# undeclared (safe default -- silence must never resolve to a green light).
# ---------------------------------------------------------------------------

_venue_tradability_cache: dict = {}


def _load_venue_tradability() -> dict:
    """Read+parse config/venue_tradability.yaml, cached per resolved path
    (not a single unconditional value) so each test's own sandboxed ROOT
    (tests/conftest.py's autouse per-test sandbox) gets its own cache entry
    instead of leaking one test's table into another test run against a
    different ROOT."""
    path = ROOT / "config" / "venue_tradability.yaml"
    cached = _venue_tradability_cache.get(path)
    if cached is not None:
        return cached
    if path.exists():
        table = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    else:
        table = {}
    table.setdefault("venues", {})
    _venue_tradability_cache[path] = table
    return table


def check_venue_tradability(venue, market_type) -> bool:
    """False if venue/market_type is undeclared, the (venue, market_type) pair
    is absent from the table, or its tradable field isn't literal True --
    "unconfirmed" and False both resolve to False, only True passes."""
    if not venue or not market_type:
        return False
    table = _load_venue_tradability()
    entry = table["venues"].get(venue, {}).get(market_type)
    if entry is None:
        return False
    return entry.get("tradable") is True


# E-061 C1.7 code-review fix: a brief copied verbatim from
# workflow_artifacts/templates/research_brief_new_pipeline.md (its placeholders
# never replaced) must never register -- registering it would queue a run that
# either crashes on nonsense values or, worse, silently treats a placeholder
# string as a real one. The sentinel is the template's own marker text.
_PLACEHOLDER_SENTINEL = "<FILL IN"


def _contains_placeholder(value) -> bool:
    """True if `value` (a str, or a nested list/dict of them) still carries
    _PLACEHOLDER_SENTINEL anywhere. Recurses into BOTH lists and dicts
    (second-round code-review fix: the first version only recursed into
    lists, so a `<FILL IN` left inside a dict -- e.g.
    machine_constraints.protocol.promotion -- was invisible to it)."""
    if isinstance(value, str):
        return _PLACEHOLDER_SENTINEL in value
    if isinstance(value, list):
        return any(_contains_placeholder(v) for v in value)
    if isinstance(value, dict):
        return any(_contains_placeholder(v) for v in value.values())
    return False


def _find_placeholder_paths(value, path: str = "") -> list:
    """Every location inside `value` (recursing into dicts and lists) that
    still carries _PLACEHOLDER_SENTINEL, as a list of dotted/bracketed
    paths -- lets a refusal message name every offending field at once
    instead of stopping at the first."""
    found = []
    if isinstance(value, str):
        if _PLACEHOLDER_SENTINEL in value:
            found.append(path or "<root>")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            found.extend(_find_placeholder_paths(v, f"{path}[{i}]"))
    elif isinstance(value, dict):
        for k, v in value.items():
            found.extend(_find_placeholder_paths(v, f"{path}.{k}" if path else str(k)))
    return found


def _normalize_symbol(sym) -> str:
    """BTC == BTCUSDT (second-round code-review fix). This repo's existing
    convention for deriving a base asset from a pair -- see
    trading-bot/execution/portfolio_info.py's own
    `symbol.replace('USDT', '')` (used repeatedly there for the same
    purpose; no dedicated helper exists there either, this mirrors that
    exact convention rather than inventing a new one). Every `symbols` value
    in this codebase (protocols/*.json, config/coin_universe.yaml) is a
    Binance-shaped pair ending in USDT regardless of actual trading venue,
    so stripping that one suffix is sufficient -- there is no second quote
    currency to handle at this project's abstraction level."""
    return sym[:-4] if isinstance(sym, str) and sym.endswith("USDT") else sym


def _lint_brief_protocol_agreement(brief_path: Path, data: dict) -> None:
    """E-061 C1.7 code-review fix: refuse a brief whose market_universe/timeframe
    disagree with the protocol machine_constraints will actually execute --
    the same drift class K3/Q1 (_lint_machine_constraints_protocol_selection's
    window_set_ref check) already refuses one level down, applied here to
    symbols/bar-size identity instead of window-set identity. Checked against
    machine_constraints.protocol (generate) directly, or against
    machine_constraints.protocol_ref's own file (pin) when that is what the
    brief carries -- the two keys are mutually exclusive (K3).

    Registration-ONLY (second-round code-review fix): called from
    _lint_new_pipeline_registration, itself called only from
    register_hypothesis -- NOT from _parse_brief_frontmatter, so a brief's
    every OTHER re-parse (materialization, dry-run, a resumed run re-reading
    its own already-registered brief) does not re-read a pinned protocol
    file or re-run this comparison. Also config_direct_authoring-gated (see
    that caller) -- this whole cross-check is specific to the "new pipeline"
    this delivery-plan slice is about.

    Timeframes compare by SECONDS (tools/timeframe.py::timeframe_seconds --
    the project's one shared bar-size arithmetic, so "60m" and "1h" agree),
    and symbols after normalizing base-asset vs full-pair naming (BTC ==
    BTCUSDT, see _normalize_symbol). The generate path's OMITTED timeframe
    defaults to "1h" -- the SAME literal default
    run_phase1_research.py::_ensure_protocol_from_constraints itself uses
    (`proto_constraint.get("timeframe", "1h")`) -- so a brief that also
    omits timeframe is compared against what will actually generate, not
    silently skipped.

    venue is not cross-checked here: machine_constraints.protocol carries
    no venue. Since O-12 (D-057) the GENERATED protocol does -- exchange,
    market_type, venue labels and the venue's symbol names, written from
    brief.venue/brief.product by tools/venue_resolver.py at generation, and
    checked against the brief again where the protocol is first used
    (_assert_protocol_matches_brief_venue).

    Raises ONLY ValueError -- the caller wraps any other exception type this
    function or its JSON read might raise (malformed machine_constraints
    shapes) into one, so register_hypothesis's `except ValueError` always
    sees a clean refusal rather than a raw crash."""
    mc = data.get("machine_constraints") or {}
    proto = mc.get("protocol")
    proto_ref = mc.get("protocol_ref")
    if proto:
        proto_symbols = proto.get("symbols")
        # SAME default _ensure_protocol_from_constraints itself uses when the
        # generate block omits timeframe -- comparing against None here would
        # silently skip the exact case a brief is most likely to get wrong.
        proto_timeframe = proto.get("timeframe", "1h")
        source = "machine_constraints.protocol"
    elif proto_ref:
        ref_path = ROOT / "protocols" / orch._path_basename_any_os(proto_ref)
        if not ref_path.exists():
            return  # _ensure_protocol_ref_pinned raises its own clear error at launch
        with open(ref_path, encoding="utf-8") as f:
            proto_obj = json.load(f) or {}
        proto_symbols, proto_timeframe = proto_obj.get("symbols"), proto_obj.get("timeframe")
        source = f"machine_constraints.protocol_ref={proto_ref!r}"
    else:
        return  # nothing pinned/generated yet -- nothing to cross-check

    market_universe = data.get("market_universe")
    if proto_symbols is not None and market_universe is not None:
        # market_universe is a list of symbols in this template, but existing
        # briefs across the corpus (and several tests) also use a single
        # comma-joined string (e.g. "BTCUSDT,ETHUSDT") or one bare symbol
        # ("BTCUSDT") -- normalize all three shapes the same way rather than
        # narrowing the field to the one shape this template happens to use.
        if isinstance(market_universe, list):
            raw_brief_symbols = market_universe
        elif isinstance(market_universe, str):
            raw_brief_symbols = [s.strip() for s in market_universe.split(",") if s.strip()]
        else:
            raw_brief_symbols = [market_universe]
        brief_symbols = {_normalize_symbol(s) for s in raw_brief_symbols}
        proto_symbols_norm = {_normalize_symbol(s) for s in proto_symbols}
        if brief_symbols != proto_symbols_norm:
            raise ValueError(
                f"{brief_path}: market_universe={sorted(raw_brief_symbols)} does not "
                f"match {source}'s symbols={sorted(proto_symbols)} -- a brief's "
                f"declared universe must agree with what it will actually backtest."
            )

    timeframe = data.get("timeframe")
    if proto_timeframe is not None and timeframe is not None:
        if timeframe_seconds(timeframe) != timeframe_seconds(proto_timeframe):
            raise ValueError(
                f"{brief_path}: timeframe={timeframe!r} does not match {source}'s "
                f"timeframe={proto_timeframe!r} -- a brief's declared bar size must "
                f"agree with what it will actually backtest."
            )


def _check_generate_protocol_has_promotion(brief_path: Path, data: dict) -> None:
    """Second-round code-review fix: registration-time half of the G7 gate.
    run_phase1_research.py::_require_pre_registered_promotion already
    refuses to GENERATE a protocol with no `promotion` block at LAUNCH --
    this refuses the same brief at REGISTRATION instead, before it even
    reaches the queue. Only applies to the generate path
    (machine_constraints.protocol); a pinned protocol_ref's promotion block
    lives in the pinned FILE already (D-3/assert_promotion_ratified checks
    that file, not this). C5.6: still the check under config_direct_authoring
    while verdict routing is live (G7 is kept there)."""
    mc = data.get("machine_constraints") or {}
    proto = mc.get("protocol")
    if isinstance(proto, dict) and not proto.get("promotion"):
        raise ValueError(
            f"{brief_path}: machine_constraints.protocol has no `promotion` block. "
            f"run_phase1_research.py's G7 gate (_require_pre_registered_promotion) "
            f"would refuse to generate this protocol at launch anyway -- refusing at "
            f"registration instead. Add median_sharpe_gt/max_abs_drawdown_pct_lt/"
            f"min_trade_count_gte/kill_median_sharpe_lt under "
            f"machine_constraints.protocol.promotion with YOUR pre-registered "
            f"thresholds (no thresholds after seeing data -- see "
            f"CLAUDE.fork.md/HYPOTHESIS.md convention)."
        )


def _check_retired_generate_protocol_promotion(brief_path: Path, data: dict) -> list:
    """C5.6 (D-043): the registration promotion check under
    config_direct_authoring AND verdict_routing_retired, where a protocol's
    promotion block decides nothing and the generated protocol carries none
    (run_phase1_research._generated_protocol_promotion drops whatever the brief
    pre-registered). Generate path only (machine_constraints.protocol).
    Returns the notes to log; raises ValueError to refuse.

      * no `promotion` key: registers, no note;
      * present but empty (`promotion: {}`, a bare `promotion:`, null):
        refused -- the shape flag-off G7 refuses, never silently read as none;
      * the abolished generic block: refused, as before;
      * any other block: registers, with a note that it is ignored."""
    mc = data.get("machine_constraints") or {}
    proto = mc.get("protocol")
    if not isinstance(proto, dict) or "promotion" not in proto:
        return []
    block = proto["promotion"]
    if not block:
        raise ValueError(
            f"{brief_path}: machine_constraints.protocol.promotion is present but empty "
            f"({block!r}). Under config_direct_authoring + verdict_routing_retired a "
            f"generated protocol needs no promotion block (C5.6, D-043) -- delete the "
            f"`promotion` key. (With verdict routing live, the G7 gate refuses an empty "
            f"block exactly as it refuses a missing one.)"
        )
    if protocol_resolution.promotion_is_generic(block):
        raise ValueError(
            f"{brief_path}: machine_constraints.protocol.promotion is the abolished generic "
            f"block {dict(block)}. Delete it: under config_direct_authoring + "
            f"verdict_routing_retired a generated protocol needs no promotion block "
            f"(C5.6, D-043), and these four numbers were never pre-registered by anyone."
        )
    return ["machine_constraints.protocol.promotion is ignored -- under "
            "config_direct_authoring + verdict_routing_retired the generated protocol "
            "carries no promotion block and nothing reads one (C5.6, D-043)"]


def _lint_new_pipeline_registration(brief_path: Path, data: dict) -> list:
    """Registration-ONLY checks for the config-direct-authoring ("new
    pipeline") path (second-round code-review fixes) -- called from
    register_hypothesis, NEVER from _parse_brief_frontmatter. Both checks
    below either read a protocol JSON file or inspect machine_constraints'
    shape, and running them on every OTHER _parse_brief_frontmatter call
    (materialization, dry-run, a resumed run re-parsing its own
    already-registered brief) would be wasted work at best and, for the
    promotion check, would re-raise on every resume of a run whose brief a
    human already registered successfully once. (C5.6: under
    config_direct_authoring + verdict_routing_retired the promotion check is
    _check_retired_generate_protocol_promotion -- no block required; under
    config_direct_authoring alone it is still "a block is required".)

    A no-op entirely when orchestrator.config_direct_authoring.enabled is
    off/absent: both checks are specific to the config-direct path this
    delivery-plan slice is about; enabling them unconditionally would be a
    real, undeclared behaviour change to every OTHER pipeline's existing,
    working briefs.

    Raises ONLY ValueError: a malformed machine_constraints shape (e.g.
    `protocol` set to a bare string instead of a dict, or a `protocol_ref`
    file that is not valid JSON) is wrapped into one clear message instead
    of escaping as a raw YAMLError/JSONDecodeError/AttributeError/TypeError
    that register_hypothesis's `except ValueError` would miss entirely.

    Returns the notes to append to the REGISTER log line (C5.6: an ignored
    promotion block); [] otherwise."""
    if not orch._config_direct_authoring_enabled():
        return []
    # C5.6: which promotion check applies depends on verdict_routing_retired too.
    # A config that cannot be read is NOT reported as a brief defect: the
    # promotion check is skipped with a note (the launch pre-flight refuses that
    # config before anything runs, and re-checks the protocol before any spend).
    try:
        promotion_retired = orch._verdict_routing_retired_enabled()
    except ValueError as exc:
        promotion_retired = None
        notes = [f"promotion check skipped -- config/campaign_config.yaml: {exc} (the "
                 f"launch pre-flight refuses this config before anything runs)"]
    else:
        notes = []
    try:
        if promotion_retired:
            notes = _check_retired_generate_protocol_promotion(brief_path, data)
        elif promotion_retired is False:
            _check_generate_protocol_has_promotion(brief_path, data)
        _lint_brief_protocol_agreement(brief_path, data)
    except ValueError:
        raise
    except (yaml.YAMLError, json.JSONDecodeError, AttributeError, TypeError, KeyError) as exc:
        raise ValueError(
            f"{brief_path}: machine_constraints is malformed ({type(exc).__name__}: "
            f"{exc}) -- refusing to register a brief whose protocol pin/generation "
            f"spec cannot be understood."
        ) from exc
    return notes


def _parse_brief_frontmatter(brief_path: Path) -> dict:
    """Extract the leading '---'-delimited YAML block from a brief .md file.
    That block IS the research_brief.yaml content (plus an optional
    machine_constraints key); everything below the closing '---' is prose
    for human readers only and is never read by the orchestrator."""
    text = brief_path.read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(
            f"{brief_path}: no leading YAML frontmatter block found "
            f"(expected the file to start with '---', then YAML, then '---')."
        )
    data = yaml.safe_load(m.group(1)) or {}
    # venue/product added 2026-08-20 (E-015 S1b): Done-when #1 requires missing
    # venue/product to fail registration outright rather than silently resolving
    # to research_only=True via check_venue_tradability's own fail-closed default
    # (still exercised directly by _materialize_run for any caller that bypasses
    # this parser, e.g. test_venue_tradability.py's direct-dict tests). No longer
    # load-bearing for holdout safety -- S3's affirmative research_only is False
    # check already closes that gap -- this is belt-and-braces at registration
    # time, which is what the rule was originally written to require.
    #
    # NOTE (E-014 naming alignment, 2026-09-10): the brief frontmatter field
    # itself stays named "product" -- it is a pre-existing, widely-used schema
    # field (research_brief.yaml template, verdict_criteria_evaluator.py,
    # test_c7ext_verdict_gates.py, and 60+ existing runs/*/artifacts/
    # research_brief.yaml files all read/write "product"). Only this module's
    # internal function/parameter naming was aligned to "market_type" to match
    # trading-bot/config/cost_model.json's axis name -- see check_venue_tradability()
    # above, which takes brief.get("product") and passes it in as market_type.
    # The tuple lives in tools/campaign_review_retired.py (slice 6c S2b review
    # fix 9) so the orchestrator's reframe-brief writer checks the same keys.
    for required in crr.REFRAME_BRIEF_REQUIRED_KEYS:
        if not data.get(required):
            raise ValueError(f"{brief_path}: frontmatter missing required field '{required}'.")

    # E-061 C1.7 second-round code-review fix: scan the WHOLE frontmatter
    # tree, not just the top-level required fields -- a placeholder left
    # inside machine_constraints (e.g. an uncommented `promotion` block whose
    # values were never filled in) is just as dangerous to register as one
    # left in strategy_domain. This runs on every _parse_brief_frontmatter
    # call (registration, materialization, dry-run, resume), unlike the two
    # config_direct_authoring-gated checks below -- a placeholder surviving
    # to launch is exactly as bad as one surviving to registration, so this
    # is intentionally NOT registration-only. DECLARED BEHAVIOUR CHANGE: any
    # existing brief anywhere in the corpus that happens to contain the
    # literal substring "<FILL IN" (in a value, not a comment -- comments
    # are never part of `data`) would now fail EVERY re-parse, not just
    # registration, where it previously only failed for the four narrower
    # required-field checks below.
    placeholder_paths = _find_placeholder_paths(data)
    if placeholder_paths:
        raise ValueError(
            f"{brief_path}: frontmatter still carries the unfilled template "
            f"placeholder sentinel '{_PLACEHOLDER_SENTINEL}' at {placeholder_paths} "
            f"-- replace every one with your own value before registering "
            f"(workflow_artifacts/templates/research_brief_new_pipeline.md's own "
            f"header comment explains each field)."
        )

    # E-061 C1.7 second-round code-review fix: the universe/timeframe
    # cross-check and the generate-path promotion check are
    # registration-ONLY (see _lint_new_pipeline_registration's own
    # docstring) -- called from register_hypothesis, not from here.
    return data


def _next_new_run_id() -> str:
    """Allocate a fresh run_id for a brand-new brief launch (no prior run_id to
    extend). Mirrors run_phase1_research._next_run_id's scan-both-sources
    approach (runs/ on disk + campaign_state.yaml's runs list) so a campaign
    started via this wrapper can never collide with a run created by directly
    invoking run_phase1_research.py/setup_run.py."""
    pattern = re.compile(r"^run_(\d+)$")
    nums = []
    runs_dir = ROOT / "runs"
    if runs_dir.exists():
        for p in runs_dir.iterdir():
            if p.is_dir():
                m = pattern.match(p.name)
                if m:
                    nums.append(int(m.group(1)))
    campaign = orch.load_campaign_state()
    for rid in campaign.get("runs", []):
        m = pattern.match(rid)
        if m:
            nums.append(int(m.group(1)))
    next_num = (max(nums) + 1) if nums else 1
    return f"run_{next_num:03d}"


def _without_retired_promotion(run_id: str, machine_constraints):
    """C5.6 (D-043) review fixes 3/4: machine_constraints without
    protocol.promotion, for a run materialized under config_direct_authoring +
    verdict_routing_retired. Nothing reads the block there, and
    pre_registration.yaml is a context file of LLM stages (and the source of
    decide_next candidates' machine_constraints), so it is dropped here, once,
    with a logged note -- never copied along. Anything else: unchanged."""
    proto = machine_constraints.get("protocol") if isinstance(machine_constraints, dict) else None
    if not (isinstance(proto, dict) and "promotion" in proto):
        return machine_constraints
    _log(f"PROMOTION {run_id}: machine_constraints.protocol.promotion dropped from "
         f"pre_registration.yaml -- under config_direct_authoring + verdict_routing_retired "
         f"nothing reads it (C5.6, D-043).")
    return {**machine_constraints,
            "protocol": {k: v for k, v in proto.items() if k != "promotion"}}


def _materialize_run(run_id: str, brief: dict, *, promotion_retired: bool = False):
    """Write runs/<run_id>/artifacts/research_brief.yaml (and pre_registration.yaml
    if the brief carries machine_constraints) into an already-scaffolded run dir.
    `promotion_retired` (C5.6): the launch pre-flight's reading of
    config_direct_authoring AND verdict_routing_retired -- then
    machine_constraints.protocol.promotion is not written
    (_without_retired_promotion)."""
    run_dir = ROOT / "runs" / run_id
    artifacts = run_dir / "artifacts"
    research_brief = {k: v for k, v in brief.items() if k != "machine_constraints"}
    venue = brief.get("venue")
    market_type = brief.get("product")
    tradable = check_venue_tradability(venue, market_type)
    research_brief["research_only"] = not tradable
    _log(f"VENUE-CHECK {run_id}: venue={venue!r} market_type={market_type!r} tradable={tradable} "
         f"research_only={not tradable}")
    orch.save_yaml(artifacts / "research_brief.yaml", research_brief)

    machine_constraints = brief.get("machine_constraints")
    if machine_constraints and promotion_retired:
        machine_constraints = _without_retired_promotion(run_id, machine_constraints)
    if machine_constraints:
        # B4/B7 rider (2026-07-16): pass_rule copy-through on the fresh_launch
        # path, mirroring _materialize_refinement_run's own extraction exactly
        # (same brief key-path -- brief["evaluation"]["pass_rule"] -- same
        # top-level pre_registration["pass_rule"] placement) -- closes the
        # documented gap this function's own prior comment named ("machine_
        # constraints-only briefs don't carry a pass_rule block yet"). One
        # gate, not two divergent ones: a fresh-launch brief that DOES
        # register a structured pass_rule is now linted and evaluated
        # identically to a refinement brief's.
        evaluation = brief.get("evaluation") or {}
        pre_registration = {
            "run_id": run_id,
            "hypothesis_id": f"{run_id}-initial",
            "registered_at": datetime.now(timezone.utc).date().isoformat(),
            "reactivation_context": (
                "First launch of this queue entry's brief lineage (not a "
                "reactivation of a prior hypothesis). machine_constraints below "
                "pin the protocol so this run cannot silently fall back to a "
                "stale campaign_state.last_escalation protocol (F4d)."
            ),
            "pass_rule": evaluation.get("pass_rule"),
            "machine_constraints": machine_constraints,
            # E-039 S4 (2026-09-12): A6.1 holdout-range declaration, moved here
            # from the `validation` stage's own quant-validation skill (which
            # used to re-read campaign_data_policy.yaml and restate this same,
            # never-changing value mid-pipeline) -- registered once, with the
            # rest of this run's pre-registered constraints, not re-declared
            # per hypothesis. Nothing in this codebase reads it back out of
            # validation_protocol.yaml's old sample_split_design location
            # (confirmed by grep); this is a pure documentation relocation.
            "sample_split_design": {
                "holdout_range": list(orch._load_holdout_range()),
                "holdout_note": (
                    "Single-use per A6.1. Evaluated only at holdout_evaluation "
                    "stage after the deflated Sharpe gate passes."
                ),
            },
        }
        # E-059 S2a (operator decision 2): a decide_next candidate's criteria are
        # written by step 1a, never inherited -- its brief carries no pass_rule
        # and says so. Mark the pre-registration pending at 1a; run_loop defers
        # the specialist_readers pre-flight until
        # run_phase1_research._write_pass_rule_from_card has written it. Absent
        # marker (every other brief): nothing added, byte-identical.
        _candidate = brief.get("candidate")
        # Slice 6c S2b review fix 1: or the BRIEF-LEVEL field a campaign-review
        # reframe brief carries (no candidate block). No other brief has it.
        if ((isinstance(_candidate, dict)
                and _candidate.get("criteria_from") == orch.PASS_RULE_PENDING_AT_1A)
                or brief.get("criteria_from") == orch.PASS_RULE_PENDING_AT_1A):
            if (pre_registration["pass_rule"] is not None
                    or machine_constraints.get("pass_rule") is not None):
                raise ValueError(
                    f"{run_id}: the brief says its criteria come from step 1a "
                    f"(criteria_from: {orch.PASS_RULE_PENDING_AT_1A}) but also "
                    f"carries a pass_rule -- refusing to materialize an inherited criterion.")
            pre_registration[orch.PASS_RULE_PENDING_KEY] = orch.PASS_RULE_PENDING_AT_1A

        # B11 (K2 kernel): materialization-time total-mapping lint. Previously
        # a no-op on this path (machine_constraints-only briefs never carried
        # a pass_rule block); now receives real content whenever the rider
        # above finds one, linted the same way a refinement brief is
        # (_materialize_refinement_run, below) -- one gate, not two divergent
        # ones.
        _violations, _warnings = orch._lint_pass_rule_total_mapping(pre_registration)
        if _violations:
            raise ValueError(
                f"{run_id}: pre_registration.yaml pass_rule failed the B11 total-mapping "
                f"lint -- refusing to materialize:\n" + "\n".join(f"  - {v}" for v in _violations)
            )
        for _w in _warnings:
            print(f"⚠️  [B11 lint] {run_id}: {_w}")

        # CUL-267: registration-time structural lint -- moves a class of
        # _evaluate_one_criterion SPEC_ERROR (unmatchable metric, invalid
        # comparator, missing null_handling) from evaluation time to here.
        _struct_violations = vce.lint_pass_rule_structure(pre_registration.get("pass_rule"))
        if _struct_violations:
            raise ValueError(
                f"{run_id}: pre_registration.yaml pass_rule failed the CUL-267 criterion "
                f"structure lint -- refusing to materialize:\n"
                + "\n".join(f"  - {v}" for v in _struct_violations)
            )

        # C5.1 (DELIVERY_REVIEW.md C4, D-013): the menu lint slice 2 promised
        # ("Once slice 2 lands, extend the same lint...") and never shipped --
        # an operator brief's own menu-shaped pass_rule used to reach this
        # point with NO menu check at all (id liveness, card_overridable,
        # scale_free threshold lock, floor no-lowering), unlike a 1a-written
        # candidate's (_pass_rule_from_card). Same gate as B11/CUL-267 above.
        _menu_path = ROOT / "config" / "criterion_menu.yaml"
        _menu = (orch.load_yaml(_menu_path) if _menu_path.exists() else {}) or {}
        _menu_violations = vce.lint_menu_shaped_pass_rule(pre_registration.get("pass_rule"), _menu)
        if _menu_violations:
            raise ValueError(
                f"{run_id}: pre_registration.yaml pass_rule failed the C5.1 menu lint "
                f"-- refusing to materialize:\n" + "\n".join(f"  - {v}" for v in _menu_violations)
            )

        # K3 (B3, §9 Q1): protocol_ref selection lint, same materialization
        # gate as B11's total-mapping lint above -- a rejected brief never
        # reaches pre_registration.yaml at all.
        _proto_violations = orch._lint_machine_constraints_protocol_selection(
            machine_constraints, pre_registration.get("pass_rule")
        )
        if _proto_violations:
            raise ValueError(
                f"{run_id}: pre_registration.yaml machine_constraints failed the K3 "
                f"protocol-selection lint -- refusing to materialize:\n"
                + "\n".join(f"  - {v}" for v in _proto_violations)
            )

        orch.save_yaml(artifacts / "pre_registration.yaml", pre_registration)


# ---------------------------------------------------------------------------
# B15: first-class registration -> schedulable queue entry. Retires the
# per-registration hand-edit to campaign_queue.yaml that H-041-C-v2 required
# (engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md B15) -- a fully-authored brief was
# previously never schedulable without a manual queue append outside any
# tool's own write path.
# ---------------------------------------------------------------------------

# E-059 S2a: the only keys `extra` may add (S1_FINDINGS_6B.md §7). Closed so a
# caller cannot use it to write `status`/`outcome` or any other field.
_REGISTER_EXTRA_KEYS = frozenset({"origin", "proposal_ref", "card_ref", "decision_ref",
                                  "brief_status", "parked_reason"})
# E-059 S2b: the statuses a registration may start in.
_REGISTER_STATUSES = ("ready", "queued")


def register_hypothesis(brief_path: Path, priority: int, notes: str, *,
                        entry_id: str | None = None, source: str = "operator_ratified",
                        relation: str | None = "new_registration",
                        extra: dict | None = None, status: str = "ready") -> int:
    """Parse `brief_path` via the EXISTING _parse_brief_frontmatter (propagates
    its own ValueError, unmodified, on a malformed brief); derive the queue id
    from the brief's filename stem; refuse (one log line, nonzero return) if
    that id already exists in the queue; otherwise append an entry mirroring
    the H-041-C-v2 entry's own field set (id, brief_path, status: ready,
    priority, source: operator_ratified, relation: new_registration, notes,
    run_ids: [], no outcome key) via the EXISTING _load_queue/_save_queue
    pair. Emits exactly one log line, success or refusal, never zero.

    E-059 S2a keyword-only arguments (defaults reproduce the entry above byte
    for byte, so the CLI and existing callers are unchanged): `entry_id`
    replaces the stem-derived id; `source` and `relation` set those fields
    (relation=None omits the key -- agent entries carry no `relation`, whose
    vocabulary is the retired routing words); `extra` adds only the E-059
    queue fields in _REGISTER_EXTRA_KEYS (a ValueError otherwise).

    E-059 S2b: `status` is `ready` (default) or `queued` -- a brief's extra
    card or a waiting R2 request, never auto-picked (a ValueError otherwise)."""
    if status not in _REGISTER_STATUSES:
        raise ValueError(f"register_hypothesis: status {status!r} not in {list(_REGISTER_STATUSES)}")
    brief_path = Path(brief_path)
    try:
        _brief_data = _parse_brief_frontmatter(brief_path)
        # E-061 C1.7 second-round code-review fix: registration-only, and
        # only under config_direct_authoring -- see that function's own
        # docstring for why this is not inside _parse_brief_frontmatter.
        _register_notes = _lint_new_pipeline_registration(brief_path, _brief_data)
    except ValueError as err:
        _log(f"REGISTER REFUSED: malformed brief {brief_path}: {err}")
        return 1

    extra = dict(extra or {})
    unknown_extra = sorted(set(extra) - _REGISTER_EXTRA_KEYS)
    if unknown_extra:
        raise ValueError(f"register_hypothesis: extra key(s) {unknown_extra} are not "
                         f"registrable (allowed: {sorted(_REGISTER_EXTRA_KEYS)})")
    new_id = entry_id if entry_id is not None else brief_path.stem
    queue = _load_queue()
    existing_ids = {e["id"] for e in queue["queue"]}
    if new_id in existing_ids:
        _log(f"REGISTER REFUSED: queue id '{new_id}' already exists (brief={brief_path}).")
        return 1

    try:
        brief_rel = brief_path.relative_to(ROOT)
    except ValueError:
        brief_rel = brief_path
    brief_rel_str = str(brief_rel).replace("\\", "/")

    entry = {
        "id": new_id,
        "brief_path": brief_rel_str,
        "status": status,
        "priority": priority,
        "source": source,
        "relation": relation,
        "notes": notes,
        "run_ids": [],
    }
    if relation is None:
        del entry["relation"]
    entry.update(extra)
    queue["queue"].append(entry)
    _save_queue(queue)
    _log(f"REGISTER: queue entry '{new_id}' appended (brief={brief_rel_str}, "
         f"priority={priority}, status={status})."
         + "".join(f" NOTE: {n}." for n in _register_notes))
    return 0


# ---------------------------------------------------------------------------
# B1 (K4 kernel): refinement_brief_path -- first-class refinement-brief
# ingestion for an ALREADY in_progress queue entry. See design note section 7.
# ---------------------------------------------------------------------------

_REQUIRED_REFINEMENT_BRIEF_KEYS = ("brief_id", "lineage", "hypothesis", "gate_definition", "evaluation")


def _parse_refinement_brief_yaml(brief_path: Path) -> dict:
    """Unlike _parse_brief_frontmatter (a '---'-delimited block inside an
    .md file), a refinement brief is a PLAIN YAML document -- confirmed
    against the real, live file at briefs/P4_ts_trend_r1_er_gate.yaml
    (design note section 7). Only validates required-top-level-key
    presence, mirroring _parse_brief_frontmatter's own error style; not
    full schema validation."""
    data = yaml.safe_load(brief_path.read_text(encoding="utf-8")) or {}
    for required in _REQUIRED_REFINEMENT_BRIEF_KEYS:
        if not data.get(required):
            raise ValueError(f"{brief_path}: refinement brief missing required field '{required}'.")
    return data


def _existing_continuation_child(run_id: str) -> str | None:
    """Reads run_id's OWN pipeline_state.yaml for an already-recorded A1
    continuation_child (i.e. internal LLM routing already fired for this
    run). Returns None if the run has no state file yet or no continuation
    recorded."""
    state_path = ROOT / "runs" / run_id / "pipeline_state.yaml"
    if not state_path.exists():
        return None
    state = orch.load_yaml(state_path) or {}
    return state.get("continuation_child")


def _materialize_refinement_run(child_id: str, brief: dict, brief_path: Path):
    """Installs a refinement_brief_path brief onto a freshly-scaffolded child
    run: byte-verbatim user_brief_verbatim.yaml (custody rule -- never
    reconstructed/paraphrased), its sha256 checksum, and a pre_registration.yaml
    carrying lineage/gate_definition/pass_rule copied verbatim (B4 copy-through
    discipline) plus machine_constraints if present. R1 (operator ruling):
    no stage-skip -- the child starts at setup_run's own default
    (hypothesis_generation); this function does not touch pending_stage."""
    run_dir = ROOT / "runs" / child_id
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    raw_bytes = brief_path.read_bytes()
    checksum = hashlib.sha256(raw_bytes).hexdigest()

    lineage = brief.get("lineage") or {}
    evaluation = brief.get("evaluation") or {}
    pre_registration = {
        "run_id": child_id,
        "hypothesis_id": brief["brief_id"],
        "registered_at": datetime.now(timezone.utc).date().isoformat(),
        "lineage": lineage,
        "gate_definition": brief.get("gate_definition"),
        "pass_rule": evaluation.get("pass_rule"),
        # E-039 S4: same A6.1 holdout-range relocation as _materialize_run
        # above -- see that function's comment for the rationale.
        "sample_split_design": {
            "holdout_range": list(orch._load_holdout_range()),
            "holdout_note": (
                "Single-use per A6.1. Evaluated only at holdout_evaluation "
                "stage after the deflated Sharpe gate passes."
            ),
        },
        "user_brief_checksum": f"sha256:{checksum}",
        "reactivation_context": (
            "Installed via refinement_brief_path (B1, K4 kernel) -- an "
            "operator-authored refinement brief, not the internal LLM "
            "routing's own proposed_brief.yaml. lineage/gate_definition/"
            "pass_rule copied verbatim from the source brief; see "
            "user_brief_verbatim.yaml for the byte-identical original."
        ),
    }
    machine_constraints = brief.get("machine_constraints")
    if machine_constraints:
        pre_registration["machine_constraints"] = machine_constraints

    # B11 (K2 kernel, 2026-07-13): materialization-time total-mapping lint,
    # checked BEFORE any file is written for this child -- a rejected brief
    # leaves only the bare setup_run() scaffold behind (same, already-tolerated
    # shape A3's reconciler flags for any other incomplete scaffold), never a
    # partially-materialized pre_registration.yaml/user_brief_verbatim.yaml
    # pair. A legacy (string-shaped) pass_rule -- e.g. run_057's own brief --
    # is not linted at all (see _lint_pass_rule_total_mapping's own docstring).
    _violations, _warnings = orch._lint_pass_rule_total_mapping(pre_registration)
    if _violations:
        raise ValueError(
            f"{child_id}: refinement brief's pass_rule failed the B11 total-mapping "
            f"lint -- refusing to materialize:\n" + "\n".join(f"  - {v}" for v in _violations)
        )
    for _w in _warnings:
        print(f"⚠️  [B11 lint] {child_id}: {_w}")

    # CUL-267: registration-time structural lint -- moves a class of
    # _evaluate_one_criterion SPEC_ERROR (unmatchable metric, invalid
    # comparator, missing null_handling) from evaluation time to here.
    _struct_violations = vce.lint_pass_rule_structure(pre_registration.get("pass_rule"))
    if _struct_violations:
        raise ValueError(
            f"{child_id}: refinement brief's pass_rule failed the CUL-267 criterion "
            f"structure lint -- refusing to materialize:\n"
            + "\n".join(f"  - {v}" for v in _struct_violations)
        )

    # C5.1 (DELIVERY_REVIEW.md C4, D-013): same menu lint as _materialize_run --
    # a refinement brief's own menu-shaped pass_rule gets the same id
    # liveness / card_overridable / scale_free / floor checks.
    _menu_path = ROOT / "config" / "criterion_menu.yaml"
    _menu = (orch.load_yaml(_menu_path) if _menu_path.exists() else {}) or {}
    _menu_violations = vce.lint_menu_shaped_pass_rule(pre_registration.get("pass_rule"), _menu)
    if _menu_violations:
        raise ValueError(
            f"{child_id}: refinement brief's pass_rule failed the C5.1 menu lint -- "
            f"refusing to materialize:\n" + "\n".join(f"  - {v}" for v in _menu_violations)
        )

    if machine_constraints:
        # K3 (B3, §9 Q1): same protocol-selection lint as _materialize_run.
        _proto_violations = orch._lint_machine_constraints_protocol_selection(
            machine_constraints, pre_registration.get("pass_rule")
        )
        if _proto_violations:
            raise ValueError(
                f"{child_id}: refinement brief's machine_constraints failed the K3 "
                f"protocol-selection lint -- refusing to materialize:\n"
                + "\n".join(f"  - {v}" for v in _proto_violations)
            )

    verbatim_path = artifacts / "user_brief_verbatim.yaml"
    verbatim_path.write_bytes(raw_bytes)
    orch.save_yaml(artifacts / "pre_registration.yaml", pre_registration)
    return checksum


# ---------------------------------------------------------------------------
# Wishlist-trigger detection (hard pause condition #3)
# ---------------------------------------------------------------------------

def _wishlist_family_names() -> list:
    names = []
    dw_path = ROOT / "config" / "detector_wishlist.yaml"
    if dw_path.exists():
        dw = orch.load_yaml(dw_path) or {}
        for c in dw.get("candidates", []):
            if c.get("family"):
                names.append(c["family"])
    fw_path = ROOT / "campaign_record" / "feed_wishlist.yaml"
    if fw_path.exists():
        fw = orch.load_yaml(fw_path) or {}
        for entry in fw.get("wishlist", []):
            if entry.get("feed_name"):
                names.append(entry["feed_name"])
    return names


def _gating_wishlist_names() -> list:
    """D-052 (2026-10-01): the wishlist names whose trigger_condition still GATES
    a campaign_review recommendation -- feed_wishlist.yaml entries only.
    config/detector_wishlist.yaml stays as a list of parked detector ideas but no
    longer gates anything: its gate existed only for the deleted A2.3 rule (no
    regime-gated hypotheses / no replacement detector until an ungated edge).
    _wishlist_family_names() still lists both files."""
    names = []
    fw_path = ROOT / "campaign_record" / "feed_wishlist.yaml"
    if fw_path.exists():
        fw = orch.load_yaml(fw_path) or {}
        for entry in fw.get("wishlist", []):
            if entry.get("feed_name"):
                names.append(entry["feed_name"])
    return names


_MISSING = object()

# 2026-07-10: sentinel for a field that predates its own schema (the record was
# written before this metric existed) -- distinct from _MISSING (the dotted
# path genuinely doesn't resolve). Both are "unresolvable" for predicate
# purposes, but neither should mask a record that fails some OTHER condition
# anyway (see _evaluate_all_of_against_records) -- only a genuinely-unknown
# field on a record that could otherwise match is a real data gap.
NOT_COMPUTED_SENTINEL = "not_computed_pre_schema"


def _get_dotted_field(d: dict, dotted_path: str):
    cur = d
    for part in dotted_path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return _MISSING
        cur = cur[part]
    return cur


def _apply_predicate_op(op: str, actual, value) -> bool:
    if op == ">":  return actual > value
    if op == ">=": return actual >= value
    if op == "<":  return actual < value
    if op == "<=": return actual <= value
    if op == "==": return actual == value
    if op == "!=": return actual != value
    if op == "in": return actual in value
    raise ValueError(f"unknown predicate op {op!r}")


def _find_wishlist_entry(family_name: str) -> dict | None:
    """Locate family_name's own entry (with its trigger_condition.predicate) in
    detector_wishlist.yaml or feed_wishlist.yaml."""
    dw_path = ROOT / "config" / "detector_wishlist.yaml"
    if dw_path.exists():
        dw = orch.load_yaml(dw_path) or {}
        for c in dw.get("candidates", []):
            if c.get("family") == family_name:
                return c
    fw_path = ROOT / "campaign_record" / "feed_wishlist.yaml"
    if fw_path.exists():
        fw = orch.load_yaml(fw_path) or {}
        for entry in fw.get("wishlist", []):
            if entry.get("feed_name") == family_name:
                return entry
    return None


def _evaluate_all_of_against_records(conditions: list, records: list, id_field: str = "id") -> dict:
    """
    Shared core: does ANY single record in `records` satisfy every condition in
    `conditions` (all_of is per-record, not independently satisfiable across
    different records)? Returns {'result', 'matched_id', 'detail'} without the
    family-name framing -- callers add that.

    2026-07-10: evaluates ALL conditions per record (no early break) so an
    unresolvable field (missing, or explicitly NOT_COMPUTED_SENTINEL) never
    masks a record that already fails some OTHER, resolvable condition. Such a
    record is a clean non-match -- it could never have satisfied all_of
    regardless of the unresolved field's true value, so it contributes to
    'false', not 'missing_field'. Only a record where every OTHER condition
    holds AND exactly the unresolved field(s) are the sole blocker is a
    genuine data gap (a record that COULD match if that field were known) --
    that's the only case that produces 'missing_field'. This closes a masking
    bug: an unrelated, pre-existing record missing a newer schema field (e.g.
    per_trade_expectancy_bps predating A3.4) could report the whole predicate
    as 'missing_field' even when the record in question was never going to
    match on other grounds (e.g. its outcome value already excludes it) --
    see campaign_knowledge_base.yaml's keltner_mean_reversion_no_edge finding
    for the case that surfaced this.
    """
    best_missing = None
    for record in records:
        failed = False
        unresolved = False
        for cond in conditions:
            actual = _get_dotted_field(record, cond["field"])
            if actual is _MISSING or actual == NOT_COMPUTED_SENTINEL:
                unresolved = True
                continue
            if not _apply_predicate_op(cond["op"], actual, cond["value"]):
                failed = True
        if not failed and not unresolved:
            return {"result": "true", "matched_id": record.get(id_field),
                    "detail": f"all {len(conditions)} condition(s) hold on record "
                              f"{record.get(id_field)!r}"}
        if failed:
            continue  # clean non-match -- an unresolved field here doesn't matter
        if unresolved and best_missing is None:
            best_missing = record.get(id_field)

    if best_missing is not None:
        return {"result": "missing_field", "matched_id": best_missing,
                "detail": f"no record satisfies all conditions; record {best_missing!r} "
                          f"could otherwise match but is missing (or has not_computed_pre_schema "
                          f"for) at least one required field -- genuine data gap"}
    return {"result": "false", "matched_id": None,
            "detail": f"checked {len(records)} record(s); none satisfy all "
                      f"{len(conditions)} condition(s)"}


def evaluate_wishlist_predicate(family_name: str) -> dict:
    """
    2026-07-10: mechanically evaluates family_name's trigger_condition.predicate
    -- closes the run_045/046 gap (a campaign_review recommendation that drew on
    a wishlist family without anyone -- human or code -- checking its
    trigger_condition at all; see
    meta_findings.daily_regime_overlay_recommended_before_a23_trigger).

    Two predicate sources are supported:
    - kb_finding: evaluated against campaign_knowledge_base.yaml's findings list
      (e.g. "has a confirmed ungated, regime-dependent edge been found").
    - campaign_queue: evaluated against config/campaign_queue.yaml's queue list
      (e.g. "has a behavioral-family brief reached status: ready" -- used by
      feed_wishlist.yaml entries whose trigger depends on what's about to be
      RUN, not on a completed finding).

    Returns {'result': 'true'|'false'|'missing_field', 'detail': str,
             'matched_finding_id': str|None}. 'true' only when ONE SINGLE
    record satisfies every all_of condition (all_of is evaluated per-record,
    not independently satisfiable across different records).
    """
    entry = _find_wishlist_entry(family_name)
    if entry is None:
        return {"result": "missing_field", "matched_finding_id": None,
                "detail": f"no wishlist entry found for family {family_name!r}"}

    predicate = (entry.get("trigger_condition") or {}).get("predicate")
    if not predicate:
        return {"result": "missing_field", "matched_finding_id": None,
                "detail": f"family {family_name!r} has no trigger_condition.predicate "
                          f"(still prose-only -- rewrite it before this can auto-evaluate)"}

    source = predicate.get("source")
    conditions = predicate.get("all_of", [])

    if source == "kb_finding":
        kb_path = ROOT / "campaign_record" / "campaign_knowledge_base.yaml"
        kb = (orch.load_yaml(kb_path) or {}) if kb_path.exists() else {}
        records = kb.get("findings", [])
    elif source == "campaign_queue":
        queue = orch.load_yaml(QUEUE_PATH) or {}
        records = queue.get("queue", [])
    else:
        return {"result": "missing_field", "matched_finding_id": None,
                "detail": f"unsupported predicate source {source!r}"}

    outcome = _evaluate_all_of_against_records(conditions, records, id_field="id")
    return {"result": outcome["result"], "matched_finding_id": outcome["matched_id"],
            "detail": outcome["detail"] + f" (source={source}, family={family_name!r})"}


_RESULT_TO_STATUS = {"true": "triggered", "false": "not_triggered", "missing_field": "data_gap"}


def evaluate_and_persist_wishlist_predicate(family_name: str) -> dict:
    """
    2026-07-10: single-authority write path for a wishlist candidate's
    trigger_condition status. detector_wishlist.yaml's own header states
    "status/last_evaluated_* fields are written back by the evaluator each
    time it runs -- do not hand-edit them" -- but evaluate_wishlist_predicate()
    itself was pure (no side effects) and NO code path ever actually wrote
    these fields back, so an orphaned `status: triggered` sat in the real file
    with no corresponding evaluator run (confirmed: grep across the repo for
    any writer of config/detector_wishlist.yaml finds none outside test
    fixtures' tmp_path sandboxes -- it was hand-authored, violating the file's
    own contract). workflow_artifacts/skills/campaign-review/SKILL.md's wishlist-gate section
    instructs the LLM-authored campaign_review stage to read this status
    field directly as textual ground truth (it cites a literal historical
    `trigger_condition.status: not_triggered` value) -- that consumer reads
    files, it cannot invoke this function live, so a persisted, freshness-
    verifiable field is structurally necessary, not optional. This is
    therefore the ONE function that may write status/last_evaluated_*/
    kb_state_hash into detector_wishlist.yaml or feed_wishlist.yaml; every
    other write is a violation of the file's own contract.

    Persists (on the SAME candidate entry the predicate came from):
      trigger_condition.status              -- triggered | not_triggered | data_gap
      trigger_condition.last_evaluated_at    -- ISO date, UTC
      trigger_condition.last_evaluated_against -- matched_finding_id or null
      trigger_condition.kb_state_hash        -- sha256 of the source file's raw
                                                 bytes at evaluation time, so a
                                                 reader can detect a persisted
                                                 status that has gone stale
                                                 relative to the current KB/queue
      trigger_condition.evaluation_note      -- the mechanical detail string

    Returns the same dict evaluate_wishlist_predicate() returns.
    """
    result = evaluate_wishlist_predicate(family_name)

    dw_path = ROOT / "config" / "detector_wishlist.yaml"
    fw_path = ROOT / "campaign_record" / "feed_wishlist.yaml"
    target_path = None
    container_key = None
    if dw_path.exists():
        dw = orch.load_yaml(dw_path) or {}
        for c in dw.get("candidates", []):
            if c.get("family") == family_name:
                target_path, container_key, entry, doc = dw_path, "candidates", c, dw
                break
    if target_path is None and fw_path.exists():
        fw = orch.load_yaml(fw_path) or {}
        for e in fw.get("wishlist", []):
            if e.get("feed_name") == family_name:
                target_path, container_key, entry, doc = fw_path, "wishlist", e, fw
                break
    if target_path is None:
        return result  # no wishlist entry found -- nothing to persist against

    predicate = (entry.get("trigger_condition") or {}).get("predicate") or {}
    source = predicate.get("source")
    if source == "kb_finding":
        source_path = ROOT / "campaign_record" / "campaign_knowledge_base.yaml"
    elif source == "campaign_queue":
        source_path = QUEUE_PATH
    else:
        source_path = None
    kb_state_hash = (
        hashlib.sha256(source_path.read_bytes()).hexdigest() if source_path and source_path.exists() else None
    )

    entry.setdefault("trigger_condition", {})
    entry["trigger_condition"]["status"] = _RESULT_TO_STATUS.get(result["result"], result["result"])
    entry["trigger_condition"]["last_evaluated_at"] = datetime.now(timezone.utc).date().isoformat()
    entry["trigger_condition"]["last_evaluated_against"] = result["matched_finding_id"]
    entry["trigger_condition"]["kb_state_hash"] = kb_state_hash
    entry["trigger_condition"]["evaluation_note"] = result["detail"]

    orch.save_yaml(target_path, doc)
    return result


def _check_wishlist_trigger(review: dict) -> str | None:
    """
    workflow_artifacts/skills/campaign-review/SKILL.md instructs campaign_review to cite (not
    necessarily consume) detector_wishlist.yaml/feed_wishlist.yaml entries as
    routine KB-question context — that happens on most reviews and is not a
    trigger. What we must catch is campaign_review actually RECOMMENDING a run
    that consumes a wishlist family (the run_045/run_046 failure mode in
    docs/00_closing_state.md section 7, "What P1a did NOT close": both were
    recommended without checking the wishlist's own trigger_condition, and
    weren't caught until later). That only happens via `reframe`
    (next_research_question targets the family) or `escalate_component`
    (already separately hard-paused by _route_escalate's new_component branch,
    checked here too for completeness/logging). So we only scan the fields
    that actually DRIVE the next action, not the whole document (which
    legitimately mentions wishlist names in its required KB-question answers).
    """
    rec = str(review.get("recommendation", "")).strip().lower()
    if rec not in ("reframe", "escalate_component"):
        return None
    parts = []
    nrq = review.get("next_research_question")
    if nrq:
        parts.append(nrq if isinstance(nrq, str) else yaml.safe_dump(nrq))
    parts.append(str(review.get("recommendation_rationale", "")))
    text = " ".join(parts).lower()
    # D-052: detector-wishlist families no longer gate (see _gating_wishlist_names)
    for name in _gating_wishlist_names():
        if name.lower() in text or name.lower().replace("_", " ") in text:
            return name
    return None


# ---------------------------------------------------------------------------
# Hard-pause classification
# ---------------------------------------------------------------------------

def _classify_human_pause(run_dir: Path, state: dict) -> str:
    flags = state.get("flags", {}) or {}
    # E-015 S3. FIRST, deliberately, and the position is load-bearing twice over.
    # (a) It must outrank the promotion_audit branch below: every route into
    #     holdout_evaluation writes promotion_audit.yaml first and holdout_result.yaml
    #     is absent at that point, so this would otherwise classify as
    #     `provisional_promote_awaiting_holdout`, whose RUNBOOK row tells the operator
    #     to run the holdout backtest by hand — the exact act this flag exists to stop.
    # (b) It must outrank the other sticky flags too. None of them is ever set back to
    #     False in code, they all fire at earlier stages than the holdout gate, and
    #     this run has by definition reached the most advanced stage — so a co-set
    #     flag here is almost always stale. Ranked below, a stale flag would replace
    #     the one message that warns against spending the seal with a row that is
    #     silent on it. A genuinely-current error masked this way is not lost: it
    #     resurfaces on the next pass once tradability is declared.
    if flags.get("research_only_unverified"):
        return "research_only_unverified"
    # Slice 6c S2a code review (item 7): run_loop's refusals under
    # orchestrator.verdict_routing_retired. Directly below the research_only hold
    # (which must outrank every sticky flag; both rows warn against running the
    # holdout) and above everything else: a refused holdout run may hold
    # promotion_audit.yaml and no holdout_result.yaml, so ranked lower it would
    # read `provisional_promote_awaiting_holdout`, whose RUNBOOK row says to run
    # the holdout backtest -- the act the flag forbids.
    if flags.get("holdout_refused_under_retired_routing"):
        return "holdout_refused_under_retired_routing"
    # Slice 6c S2d: the holdout unlock's three pauses, beside the refusal above
    # and for the same reason -- a run here may carry a stale profit_bars_reached
    # flag, which must not mask a refused, awaiting or inconclusive spend.
    if flags.get(orch.HOLDOUT_UNLOCK_REFUSED_FLAG):
        return orch.HOLDOUT_UNLOCK_REFUSED_FLAG
    if flags.get(orch.HOLDOUT_AWAITING_RESULT_FLAG):
        return orch.HOLDOUT_AWAITING_RESULT_FLAG
    if flags.get(orch.HOLDOUT_RESULT_INCONCLUSIVE_FLAG):
        return orch.HOLDOUT_RESULT_INCONCLUSIVE_FLAG
    # Slice 6c S2d review fixes 3-5: a spent seal whose ending is withheld.
    if flags.get(orch.HOLDOUT_SPENT_WITHOUT_UNLOCK_FLAG):
        return orch.HOLDOUT_SPENT_WITHOUT_UNLOCK_FLAG
    if flags.get(orch.HOLDOUT_RESULT_UNBOUND_FLAG):
        return orch.HOLDOUT_RESULT_UNBOUND_FLAG
    if flags.get(orch.HOLDOUT_RESULT_RELABELLED_FLAG):
        return orch.HOLDOUT_RESULT_RELABELLED_FLAG
    if flags.get("campaign_review_refused_under_retired_routing"):
        return "campaign_review_refused_under_retired_routing"
    # Slice 6c S2b: campaign review said stop (orchestrator.verdict_routing_retired).
    # Beside the two refusals above, which share its origin; a stale lower flag
    # (e.g. profit_bars_reached from earlier in this run) must not mask a stop.
    if flags.get(crr.CAMPAIGN_REVIEW_TERMINATE_FLAG):
        return crr.CAMPAIGN_REVIEW_TERMINATE_FLAG
    if flags.get("no_signal_artifact_flagged"):
        return "no_signal_artifact"
    if flags.get("conformance_violation") or state.get("conformance_violations"):
        return "conformance_gate_failure"
    if flags.get("regime_misattribution_flagged"):
        return "regime_misattribution"
    if flags.get("component_execution_error_flagged"):
        return "component_execution_error"
    if flags.get("kb_reactivation_violation") or state.get("kb_reactivation_violations"):
        return "kb_reactivation_violation"
    # PRE-EXISTING GAP, fixed here because it sits in this function and its RUNBOOK
    # row already exists: run_phase1_research sets this flag on two human-pause paths
    # (in _route_verdict_interpretation and its A8.6 sibling; no line numbers, they
    # move) but nothing read it, so the reason string was unreachable and those pauses
    # surfaced as `human_pause_unclassified`.
    if flags.get("pass_rule_evaluation_disagreement"):
        return "pass_rule_evaluation_disagreement"
    # E-032 S2c (operator ruling 2026-08-23): set by
    # run_phase1_research._route_post_innovation_expansion after the 4th
    # CONSECUTIVE anti-adjacency gate REFUSE for one lineage step, only when
    # orchestrator.anti_adjacency_retry.enabled is true. Named here so this
    # escalation reads as itself in campaign_log.md / halt_history instead of
    # falling through to human_pause_unclassified -- same pattern as every
    # other flag-keyed reason in this function. Not in _QUARANTINE_SAFE_
    # REASONS or _REQUEUEABLE_QUARANTINE_REASONS below: this is a genuine
    # must-escalate per the operator's own ruling, not an auto-recoverable
    # engineering failure. E-036 S2a (2026-09-27) RETIRED the writer (the
    # anti_adjacency_retry flag and _route_post_innovation_expansion's gate
    # call, S1_FINDINGS_SLICE8.md §1): nothing sets this flag any more. The
    # branch stays only so a pipeline_state.yaml written before then still
    # classifies as itself.
    if flags.get("anti_adjacency_gate_exhausted"):
        return "anti_adjacency_gate_exhausted"
    # E-034 S3. Set by run_phase1_research._route_post_variant_selection when
    # the anti-adjacency gate REFUSEs the CHOSEN VARIANT (the new, later call
    # site -- distinct from anti_adjacency_gate_exhausted above, which is the
    # EARLIER, pre-validation checkpoint's 4-retry exhaustion). Deliberately a
    # DIFFERENT reason string: this checkpoint escalates on the FIRST REFUSE,
    # after validation + backtest_specification have already run, so an
    # operator scanning halts can tell "refused early, cheap" apart from
    # "refused late, after two stages' spend" at a glance. Named here so this
    # escalation reads as itself in campaign_log.md / halt_history instead of
    # falling through to human_pause_unclassified -- same pattern as every
    # other flag-keyed reason in this function. Not in _QUARANTINE_SAFE_
    # REASONS or _REQUEUEABLE_QUARANTINE_REASONS below: a genuine
    # must-escalate, not an auto-recoverable engineering failure.
    if flags.get("variant_anti_adjacency_gate_refused"):
        return "variant_anti_adjacency_gate_refused"
    # E-061 C2 S2c (C2_S1_FINDINGS.md G12): set by run_phase1_research's
    # _variant_step2_retry_or_pause when Step 2's output is still invalid after
    # its one retry -- the variant shape (3-4 variants, one base, >= 1 design,
    # 1-2 asset, one coin each), or 5a refused a variant's config (a patch that
    # does not apply, unresolved manifest paths, a V-code other than a missing
    # class). Before variant_gate_insufficient: both stop the run before the
    # data gate, so the floor's label only ever reads a data or class loss.
    # A human decides; never quarantine-safe.
    if flags.get("variant_shape_invalid"):
        return "variant_shape_invalid"
    if flags.get("variant_config_error"):
        return "variant_config_error"
    # D-051: set by run_phase1_research._route_block_manifest_check when 1b's
    # base config still breaks the graded-forecast rule after its one retry (or
    # at once for a decide_next pass-through config 1b cannot change). Stops
    # before Step 2; a human decides; never quarantine-safe.
    if flags.get("forecast_rule_violation"):
        return "forecast_rule_violation"
    # E-033.1 Slice 4b (2026-09-22): set by run_phase1_research's
    # data_availability_gate elif-branch in run_loop when, after the
    # per-variant data-availability gate has run, fewer than 3 variants
    # remain "validated" in artifacts/variants/index.yaml. Deliberately a
    # DISTINCT flag from idea_status (S1_FINDINGS.md §8's "idea_status
    # collision" -- that field already means something different: the
    # criteria-grid's own validated/refuted/inconclusive rollup, written by
    # _build_idea_status_artifact AFTER backtests complete). This is a
    # precondition failure that happens BEFORE protocol_execution/the grid
    # ever run, so -- unlike profit_bars_reached below -- it can never
    # co-occur with promotion_audit.yaml and does not need to outrank the
    # promotion_audit block; placed here purely to mirror the other
    # early-pipeline sticky-flag branches immediately above it.
    if flags.get("variant_gate_insufficient"):
        return "variant_gate_insufficient"
    # E-046a Slice 5b-ii-B (orchestrator.specialist_readers.enabled): set by
    # run_phase1_research.determine_post_specialist_readers_route when the grid's
    # idea_status.yaml reads `inconclusive` -- delivery_plan_v26.md slice 2's
    # "inconclusive -> human_pause (reason: inconclusive_grid)". A human decides;
    # never quarantine-safe. It cannot co-occur with promotion_audit.yaml (an
    # inconclusive grid never reaches the promote branch), so it needs no rank
    # above that block; placed here beside the other late-pipeline sticky flags.
    if flags.get("inconclusive_grid"):
        return "inconclusive_grid"
    # delivery_plan_v26.md 0.2 (item 2) -- the branch-3 stop
    # (orchestrator.profit_bars_file.enabled, off by default). Must outrank the
    # promotion_audit block below for the exact same reason research_only_unverified
    # does (see that flag's own comment at the top of this function):
    # run_phase1_research._dispatch_verdict_route writes promotion_audit.yaml BEFORE
    # setting this flag, on the SAME promote branch, so by the time this flag is set
    # promotion_audit.yaml already exists and holdout_result.yaml does not -- without
    # this check ranking first, every profit_bars_reached pause would misclassify as
    # `provisional_promote_awaiting_holdout`, whose RUNBOOK row tells the operator to
    # run the holdout backtest, exactly the act this stop exists to gate before.
    # The same flag is also raised by the per-backtest check
    # (orchestrator.profit_bars_every_backtest.enabled), in the route after
    # regroup_record and before the grid route -- this branch classifies it
    # identically; no new reason, no new row (RUNBOOK §3 has both origins).
    if flags.get("profit_bars_reached"):
        return "profit_bars_reached"
    # E-061 C1.4 / C1.5: process_once halts on these directly, with the reason
    # named (it never needs this function for them). Named here so a later
    # classification of the same state reads as itself. Ranked ABOVE the
    # artifact-based reasons below (third-round review fix 8): a flag set by
    # THIS halt must win over an old artifact (e.g. a refinement_notes.yaml from
    # an earlier data block). Staleness is handled by clearing, not by rank: a
    # successful --resume sets all three back to false (_clear_run_halt_flags).
    if flags.get(STAGE_EXCEPTION_HALT):
        return STAGE_EXCEPTION_HALT
    if flags.get(PROTOCOL_PREFLIGHT_HALT):
        return PROTOCOL_PREFLIGHT_HALT
    if flags.get(LAUNCH_EXCEPTION_HALT):
        return LAUNCH_EXCEPTION_HALT

    artifacts = run_dir / "artifacts"
    audit_path = artifacts / "promotion_audit.yaml"
    holdout_path = artifacts / "holdout_result.yaml"
    if audit_path.exists():
        if not holdout_path.exists():
            return "provisional_promote_awaiting_holdout"
        hr = orch.load_yaml(holdout_path) or {}
        if str(hr.get("status", "")).lower() not in ("pass", "fail"):
            return "provisional_promote_holdout_inconclusive"

    decision_path = artifacts / "decision.yaml"
    if decision_path.exists():
        d = orch.load_yaml(decision_path) or {}
        if d.get("status") == "component_gap":
            return "component_gap"

    esc_path = artifacts / "escalation_request.yaml"
    if esc_path.exists():
        e = orch.load_yaml(esc_path) or {}
        if e.get("target") == "new_component":
            return "new_component_escalation"

    refine_path = artifacts / "refinement_notes.yaml"
    if refine_path.exists():
        r = orch.load_yaml(refine_path) or {}
        if (r.get("decision") or {}).get("implementation_allowed") is False:
            return "data_block_hitl"

    return "human_pause_unclassified"


def _hard_pause_reason(run_dir: Path, state: dict):
    """Returns (reason, detail) if the campaign must halt, else None."""
    status = state.get("status", "")
    pending = state.get("pending_stage") or ""

    if status == "failed":
        # K3/§9 Q2: check the flag-based signal BEFORE falling back to the generic
        # reason -- otherwise a RuntimeError raised by _resolve_protocol_path's B10
        # hard-fail (which sets this flag via update_state before raising) would
        # always classify as the uninformative "unhandled_exception", indistinguishable
        # from any other engineering failure in this file.
        flags = state.get("flags", {}) or {}
        if flags.get("stale_escalation_unclaimed"):
            return "stale_escalation_unclaimed", str(state.get("last_error", ""))[:300]
        return "unhandled_exception", str(state.get("last_error", ""))[:300]

    if pending == "rejected_budget_exceeded":
        return "budget_breaker", ""

    # Slice 6c S2b review fixes 2+4 and 6, reached only by a run whose review the
    # verdict_routing_retired trigger started (flag-off runs never carry the
    # marker or the flag, so neither branch can fire for them):
    #   * run_loop's budget stop leaves status=rejected_budget_exceeded with the
    #     review still pending -- a classified halt, never a silent DONE;
    #   * campaign review said stop -- it outranks the wishlist check below, so
    #     a terminate is never reported as a wishlist question.
    if state.get(orch.CAMPAIGN_REVIEW_TRIGGER_KEY):
        if status == "rejected_budget_exceeded" and pending == "campaign_review":
            return "budget_breaker", ("campaign_review stopped by the weighted token budget; the "
                                      "review is still pending (it never completed, so the "
                                      "cadence carries it forward)")
        if status == "paused_for_human" and (state.get("flags") or {}).get(
                crr.CAMPAIGN_REVIEW_TERMINATE_FLAG):
            return crr.CAMPAIGN_REVIEW_TERMINATE_FLAG, ""

    cr_path = run_dir / "artifacts" / "campaign_review.yaml"
    if cr_path.exists():
        review = orch.load_yaml(cr_path) or {}
        matched = _check_wishlist_trigger(review)
        if matched:
            # 2026-07-10: mechanically evaluate the trigger instead of always
            # hard-pausing for human judgment (the run_045/046 gap this whole
            # check exists to close). true -> fall through, let the normal
            # reframe/escalate routing continue autonomously (component_gap
            # remains its own separate, legitimate pause if backtest_specification
            # later finds a genuinely missing engine piece). false/missing_field
            # -> still pause, but with the mechanical verdict in the detail so a
            # human doesn't have to re-derive it by hand.
            verdict = evaluate_wishlist_predicate(matched)
            if verdict["result"] == "true":
                pass  # do not pause -- predicate fired, proceed autonomously
            elif verdict["result"] == "missing_field":
                return "wishlist_trigger_data_gap", f"{matched}: {verdict['detail']}"
            else:
                return "wishlist_trigger", f"{matched}: {verdict['detail']}"

    if status == "paused_for_human" or pending == "human_pause":
        reason = _classify_human_pause(run_dir, state)
        if reason == orch.HOLDOUT_UNLOCK_REFUSED_FLAG:
            # Slice 6c S2d: the HALT line names the refusal code (RUNBOOK §3 has
            # one row per code). Every other reason: unchanged, no detail.
            refusal = state.get(orch.HOLDOUT_UNLOCK_REFUSAL_KEY) or {}
            return reason, (f"{refusal.get('code')}: {refusal.get('detail')}"[:300]
                            if refusal else "")
        return reason, ""

    return None


def _append_halt_history(run_dir: Path, state: dict, reason: str, detail: str = "",
                         quarantine: dict | None = None, parked: dict | None = None) -> None:
    """E-030 S1 durable-halt-record fix. `pipeline_state.yaml`'s `last_error` is
    written in full at halt time (run_loop's except-block, `last_error=str(e)`,
    untruncated) but RUNBOOK.md section 4's own documented resume procedure has the
    operator null it on every resume (every reason except data_block_hitl) -- and
    _hard_pause_reason's own return value truncates it to 300 chars for the
    campaign_log.md HALT line before this function ever sees it. Neither loss is a
    bug in isolation; together they meant halt #7 in the E-030 S1 taxonomy
    (46.85h, the single largest halt in the campaign's history) left no recoverable
    cause anywhere on disk.

    Modeled on `completed_stages`/`audit_log`, the two fields on this same file that
    already accumulate across a run's life instead of being overwritten -- one more
    accumulating field here, not a new artifact type. Called BEFORE any resume step
    (manual today, possibly automatic once S2 lands) can touch `last_error`/`flags`,
    so the append captures what the reset would otherwise destroy. Reads
    `state["last_error"]` directly (untruncated), not the truncated `detail` the
    caller may also be about to log to campaign_log.md.

    E-030 S2a: `quarantine` carries the R6 quarantine record when a halt was
    quarantined instead of escalated. It rides on THIS entry rather than on the
    queue entry or in a new artifact for two structural reasons: (a) R6's minimum
    fields -- reason, untruncated failure text, `pending_stage` at halt, the `flags`
    dict verbatim -- are already exactly what this snapshot captures, so a separate
    record would duplicate four of six fields and could drift from them; (b)
    `config/campaign_queue.yaml` entries are governed by a CLOSED schema
    (`tools/record_schema.py`'s QUEUE_ENTRY_SCHEMA, which permits neither an unknown
    field nor a nested mapping inside a permitted one), so the record structurally
    cannot live there. Additive, not invasive. `None` for an escalated halt, which
    is every halt while `quarantine_enabled` is false.
    """
    history = list(state.get("halt_history") or [])
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reason": reason,
        "detail": detail,
        "last_error": state.get("last_error"),
        "pending_stage": state.get("pending_stage"),
        "flags": dict(state.get("flags") or {}),
        "completed_stages": list(state.get("completed_stages") or []),
        "counters": dict(state.get("counters") or {}),
    }
    if quarantine is not None:
        record["quarantine"] = quarantine
    if parked is not None:
        # Slice 6c S2c: the park marker, so the instrument can tell a park (the
        # loop continued) from an escalated halt (it stopped).
        record["parked"] = parked
    history.append(record)
    orch.update_state(path=run_dir, halt_history=history)


# ---------------------------------------------------------------------------
# E-030 S2a — quarantine + escalate halt policy
#
# SCOPE, STATED UP FRONT BECAUSE THE EPIC'S OWN DONE-WHEN IS WIDER THAN THIS:
# EPIC.md Done-when #1 describes a retry mechanism AND a quarantine mechanism.
# This is the quarantine half only. The taxonomy's R2 is why: "The one proven-
# retryable signature is an exact string match, and it is already implemented that
# way" -- the single evidenced retry-safe case (the claude_agent_sdk==0.2.82
# result-misclassification message) is already retried at the STAGE level inside
# run_phase1_research._invoke_agent_with_yaml_retry (ledger A11, commit 9bf2a4cf).
# There is no second evidenced campaign-level retry-safe signature to wire up, and
# inventing a heuristic for one now would be exactly the reason-code-keyed guessing
# R2 exists to forbid. So no retry machinery is built here and none is stubbed.
#
# The default is ESCALATE. Quarantine is the narrow exception, and its membership
# comes from the S1 taxonomy's per-halt evidence, not from judgment applied here.
# ---------------------------------------------------------------------------

# Quarantine-safe, per E-030/artifacts/s1_halt_taxonomy.md's per-halt classification:
#   no_signal_artifact          -- halts #6 (run_054). F5c: a component never fired
#                                  or errored on every bar. The taxonomy states it
#                                  plainly: "an engineering fact, explicitly not a
#                                  scientific result."
#   component_execution_error   -- halts #8 (misreported), #9, #13. A real engine
#                                  bug; no retry can fix it and the queue has no
#                                  reason to stop.
#   component_gap               -- halt #2 (run_053). Re-queueable, not terminal.
#   new_component_escalation    -- no occurrence among the 14 measured halts; paired
#                                  with component_gap by R9 because it is the same
#                                  situation reached from a different stage (the
#                                  engine lacks a piece), and its queue treatment is
#                                  identical.
# EVERYTHING else escalates, including unhandled_exception (R2: 6 of 14 halts, at
# least four unrelated root causes) and every reason in R1's integrity list.
_QUARANTINE_SAFE_REASONS = frozenset({
    "no_signal_artifact",
    "component_execution_error",
    "component_gap",
    "new_component_escalation",
})

# R9: these two quarantine as RE-QUEUEABLE -- `blocked_on_component:<name>` on the
# queue entry's `status`, never `done`. The hypothesis is not defective; the engine
# is simply missing a piece, so the run survives for whoever writes that piece.
# `_select_entry` already skips every `blocked_on_*` entry ("`blocked_on_*` / `done`
# / `paused:*` entries are never auto-selected" -- its own docstring, unchanged by
# this story), and `blocked_on_.+` is already an accepted QUEUE_STATUS shape in
# tools/record_schema.py. Nothing in the selection path needs to change.
_REQUEUEABLE_QUARANTINE_REASONS = frozenset({"component_gap", "new_component_escalation"})

# E-060 S3b: a composition run -- an R1 entry (queue origin `composition`) or
# a reader patch on a composite (7.5: research_brief candidate.composition,
# queue origin `reader`; review fix 3) -- ending in one of these engineering
# faults pauses the campaign as `paused:composition_failed` (RUNBOOK §3) --
# never quarantined, never retried by code. Any other pause of a composition
# run (e.g. the branch-3 profit_bars_reached stop) keeps its own reason.
COMPOSITION_ORIGIN = _composition_names.ORIGIN_COMPOSITION
COMPOSITION_FAILED_REASON = "composition_failed"


def _is_composition_run(entry: dict, run_dir: Path) -> bool:
    """R1 entry, or a run whose research_brief.yaml carries candidate.composition
    (only composition_runs writes either)."""
    if entry.get("origin") == COMPOSITION_ORIGIN:
        return True
    return orch._composition_candidate(run_dir) is not None
_COMPOSITION_FAULT_REASONS = _QUARANTINE_SAFE_REASONS | frozenset(
    {"unhandled_exception", "stale_escalation_unclaimed", "budget_breaker"})

# R8/R6: the one outcome value a quarantine may write. Registered as non-verdict-
# bearing in tools/verdict_criteria_evaluator._NON_VERDICT_OUTCOMES (see that entry's
# comment) so _save_queue's provenance gate admits it without a
# pass_rule_evaluation_ref -- because it asserts nothing about the hypothesis.
# Deliberately NOT `completed_rejected`, which is a scientific claim.
_QUARANTINE_OUTCOME = "quarantined_engineering_failure"

# R11's cross-check table. Mirrors _classify_human_pause's sticky-flag branches in
# ITS OWN ORDER, mapping each flag (and the two state-key counterparts that function
# reads alongside their flags) to the reason it produces. Duplicating that order is a
# rot risk, so test_halt_quarantine_policy.py drives _classify_human_pause with each
# flag in isolation and asserts the mapping still holds -- a static table checked by
# execution, rather than a second hand-maintained list nobody verifies.
_PAUSE_FLAG_TO_REASON = (
    ("research_only_unverified", "research_only_unverified"),
    # Slice 6c S2a code review (item 7). Mirrors the two branches directly below
    # research_only_unverified in _classify_human_pause.
    ("holdout_refused_under_retired_routing", "holdout_refused_under_retired_routing"),
    # Slice 6c S2d: mirrors the three branches directly below that one.
    (orch.HOLDOUT_UNLOCK_REFUSED_FLAG, orch.HOLDOUT_UNLOCK_REFUSED_FLAG),
    (orch.HOLDOUT_AWAITING_RESULT_FLAG, orch.HOLDOUT_AWAITING_RESULT_FLAG),
    (orch.HOLDOUT_RESULT_INCONCLUSIVE_FLAG, orch.HOLDOUT_RESULT_INCONCLUSIVE_FLAG),
    (orch.HOLDOUT_SPENT_WITHOUT_UNLOCK_FLAG, orch.HOLDOUT_SPENT_WITHOUT_UNLOCK_FLAG),
    (orch.HOLDOUT_RESULT_UNBOUND_FLAG, orch.HOLDOUT_RESULT_UNBOUND_FLAG),
    (orch.HOLDOUT_RESULT_RELABELLED_FLAG, orch.HOLDOUT_RESULT_RELABELLED_FLAG),
    ("campaign_review_refused_under_retired_routing",
     "campaign_review_refused_under_retired_routing"),
    # Slice 6c S2b: mirrors the branch directly below those in _classify_human_pause.
    (crr.CAMPAIGN_REVIEW_TERMINATE_FLAG, crr.CAMPAIGN_REVIEW_TERMINATE_FLAG),
    ("no_signal_artifact_flagged", "no_signal_artifact"),
    ("conformance_violation", "conformance_gate_failure"),
    ("regime_misattribution_flagged", "regime_misattribution"),
    ("component_execution_error_flagged", "component_execution_error"),
    ("kb_reactivation_violation", "kb_reactivation_violation"),
    ("pass_rule_evaluation_disagreement", "pass_rule_evaluation_disagreement"),
    # E-032 S2c. Mirrors _classify_human_pause's branch for this flag, which
    # sits immediately after pass_rule_evaluation_disagreement in that
    # function's own order -- see this flag's comment there. Currently inert
    # (deliberately outside _QUARANTINE_SAFE_REASONS, so _flag_ambiguity
    # never fires for it), but the table's own docstring promises it mirrors
    # every sticky-flag branch, so its absence here was real drift (FIX 6,
    # review 2026-08-24).
    ("anti_adjacency_gate_exhausted", "anti_adjacency_gate_exhausted"),
    # E-034 S3. Mirrors _classify_human_pause's branch for this flag, which
    # sits immediately after anti_adjacency_gate_exhausted in that function's
    # own order -- see this flag's comment there. Also deliberately outside
    # _QUARANTINE_SAFE_REASONS/_REQUEUEABLE_QUARANTINE_REASONS. Added here
    # from the start (not as a later fix) precisely BECAUSE the 2026-08-24
    # bug-fix pass (FIX 6) added a regression test
    # (test_every_known_sticky_flag_branch_has_a_pause_flag_to_reason_entry)
    # specifically to catch a future omission of exactly this kind.
    ("variant_anti_adjacency_gate_refused", "variant_anti_adjacency_gate_refused"),
    # E-061 C2 S2c. Mirrors the two branches directly above
    # variant_gate_insufficient in _classify_human_pause.
    ("variant_shape_invalid", "variant_shape_invalid"),
    ("variant_config_error", "variant_config_error"),
    # D-051. Mirrors _classify_human_pause's branch for this flag, which sits
    # immediately after variant_config_error there.
    ("forecast_rule_violation", "forecast_rule_violation"),
    # E-033.1 Slice 4b. Mirrors _classify_human_pause's branch for this flag,
    # which sits immediately after variant_config_error (E-061 C2 S2c) in
    # that function's own order -- see this flag's comment there.
    ("variant_gate_insufficient", "variant_gate_insufficient"),
    # E-046a Slice 5b-ii-B. Mirrors _classify_human_pause's branch for this
    # flag, which sits immediately after variant_gate_insufficient there.
    ("inconclusive_grid", "inconclusive_grid"),
    # Profit-bars branch-3 stop (orchestrator.profit_bars_file.enabled). Mirrors
    # _classify_human_pause's branch for this flag -- see that flag's comment
    # there for why it must rank above the promotion_audit block. CODE-REVIEW
    # FIX (2026-09-21): this entry was originally omitted, the exact drift
    # test_every_known_sticky_flag_branch_has_a_pause_flag_to_reason_entry
    # exists to catch -- the test's own known_sticky_flags tuple was also
    # missing this flag, so it did not catch itself; both fixed together.
    ("profit_bars_reached", "profit_bars_reached"),
    # E-061 C1.4 / C1.5. Mirrors the three branches directly below
    # profit_bars_reached in _classify_human_pause (a stale one alongside a
    # quarantine-safe reason escalates -- R11 -- rather than quarantines).
    (STAGE_EXCEPTION_HALT, STAGE_EXCEPTION_HALT),
    (PROTOCOL_PREFLIGHT_HALT, PROTOCOL_PREFLIGHT_HALT),
    (LAUNCH_EXCEPTION_HALT, LAUNCH_EXCEPTION_HALT),
    # _hard_pause_reason reads this one BEFORE _classify_human_pause is ever called
    # (while status == "failed"); it is must-escalate in its own right, so its
    # presence alongside anything else is unambiguously a reason not to quarantine.
    ("stale_escalation_unclaimed", "stale_escalation_unclaimed"),
)
_PAUSE_STATE_KEY_TO_REASON = (
    ("conformance_violations", "conformance_gate_failure"),
    ("kb_reactivation_violations", "kb_reactivation_violation"),
)


def _quarantine_enabled() -> bool:
    """E-030 S2a gate. False (escalate exactly as before) when the key, the section
    or the file is absent -- silence is never a green light for a behavior change.

    Read via ROOT rather than a source-file-relative path so the test sandbox
    (tests/conftest.py's autouse guard patches ROOT) can seed its own value;
    run_phase1_research._load_symbol_correlation reads campaign_config.yaml the same
    way. In the real repository the two paths are identical."""
    path = ROOT / "config" / "campaign_config.yaml"
    if not path.exists():
        return False
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    halt_policy = ((cfg.get("orchestrator") or {}).get("halt_policy") or {})
    return bool(halt_policy.get("quarantine_enabled", False))


def _flag_ambiguity(state: dict, reason: str) -> str | None:
    """R11. Returns a human-readable explanation when the `flags` dict does not
    unambiguously support `reason`, else None. An ambiguous halt is escalated, never
    quarantined -- and the fact that the check fired is logged (see process_once).

    THE EVIDENCE. Halt #8 in the taxonomy is a confirmed misreport, documented by
    date in RUNBOOK.md section 4: a fresh `component_execution_error_flagged: true`
    pause surfaced as `no_signal_artifact` because #6's flag had never been cleared,
    and _classify_human_pause checks the stale higher-priority flag first. Both of
    those reasons are on the quarantine-safe list, and they carry DIFFERENT trial
    accounting (R7) -- so acting on the reported code would have applied the wrong
    one, silently.

    THE RULE, and why it is not the literal one-directional wording. Checking only
    for a flag of HIGHER priority than the returned reason is vacuous by
    construction: _classify_human_pause returns the highest-priority set flag, so
    nothing higher can exist by the time this runs. The bug it needs to catch runs
    the other way -- a stale HIGH flag masking a live LOW one. So the rule is
    symmetric: quarantine only when the truthy classifier-read flags are either
    none at all (an artifact-derived reason such as component_gap) or exactly the
    single flag that maps to this reason. Any other shape escalates. That is
    strictly safer in both directions and it is what the measured incident requires.
    """
    flags = state.get("flags", {}) or {}
    set_reasons = {mapped for flag, mapped in _PAUSE_FLAG_TO_REASON if flags.get(flag)}
    set_reasons |= {mapped for key, mapped in _PAUSE_STATE_KEY_TO_REASON if state.get(key)}

    if not set_reasons:
        # An artifact-derived reason (component_gap / new_component_escalation is
        # reached only when no sticky flag is set at all). Unambiguous.
        return None
    if set_reasons == {reason}:
        return None
    others = sorted(set_reasons - {reason})
    return (f"flags on pipeline_state.yaml resolve to {sorted(set_reasons)} while the halt "
            f"reported {reason!r}; the extra flag(s) {others} may be stale from an earlier "
            f"resolved pause (taxonomy halt #8 fingerprint), so the reason code is not "
            f"reliable evidence of what went wrong")


def _repeat_quarantine(state: dict, reason: str) -> dict | None:
    """E-030 S3 / taxonomy R4. Returns the PRECEDING halt_history entry when this
    halt is the second occurrence in a row of the same reason code on the same run
    AND the first one was auto-quarantined; None otherwise. A non-None return means
    "do not quarantine again -- escalate".

    R4 VERBATIM: *"Same reason code twice in a row on the same run => stop retrying,
    escalate. Supported by both repeat pairs in the record (#4/#5 on run_053,
    #13/#14 on run_059) and consistent with the existing local precedent -- the A11
    SDK retry fires once and re-raises on a second occurrence."* R4 was written for
    retry; S2b (retry) does not exist and stays unbuilt (no second evidenced
    retry-safe signature -- R2). Quarantine is the auto-action that DOES exist, so
    this is R4 applied to it, and the wording here says so rather than letting a
    reader believe retry-vs-escalate was built.

    THE EVIDENCE, on point: halts #13 and #14 are both `component_execution_error`
    (quarantine-safe), both on run_059, back to back. #13 was a real engine bug
    (`CandleBuilder._align()` tz round-trip) fixed by a human at the confirmed site;
    #14 then needed a state-only human intervention -- no commit exists in its
    window -- after which the run reached terminal in 2m17s. A policy that
    quarantines the same reason a second time in a row is not recovering, it is
    laundering a repeating fault into an outcome nobody looks at.

    ADJACENCY, stated because "in a row" needs a definition and this one is tested:
    only `halt_history[-1]` is consulted -- the IMMEDIATELY preceding halt on this
    run. Any other halt in between (of any reason) breaks the chain, because the
    intervening halt is itself evidence the run's situation changed. This function
    runs BEFORE the current halt is appended, so `[-1]` is genuinely the previous
    one.

    THE `quarantine` KEY IS REQUIRED, not just the reason match. A previous
    same-reason halt that ESCALATED means a human already looked at it and resumed;
    that is a different situation from the loop having silently auto-actioned it,
    and R4's target is the silent repeat. The key's presence is the only durable
    on-disk record of "the loop, not a human, handled the last one" (S2a writes it
    on the quarantine path and nowhere else).
    """
    history = state.get("halt_history") or []
    if not history:
        return None
    previous = history[-1]
    if not isinstance(previous, dict):
        return None
    if previous.get("reason") != reason:
        return None
    if "quarantine" not in previous:
        return None
    return previous


_COMPONENT_NAME_RE = re.compile(r"\b([A-Z][A-Za-z0-9_]*Component)\b")


def _blocked_component_name(run_dir: Path, detail: str) -> str:
    """R9's `<name>` for `blocked_on_component:<name>`, best-effort and honest about it.

    No artifact in this pipeline carries a dedicated component-name field: a
    component_gap `decision.yaml` holds only stage/status/hypothesis_id/run_id/
    rationale/blocking_issues (verified against runs/run_047 and runs/run_057, the
    two component_gap decisions on disk), and a new_component
    `escalation_request.yaml` holds target/reason. The name that resolved halt #2
    (`MacdHistogramCrossoverComponent`) survives only in prose -- the human's own
    RESUME line. So this scans the prose sources for a `*Component` identifier and
    falls back to a loud placeholder.

    Getting the name wrong costs nothing structural: the status is still
    `blocked_on_*`, `_select_entry` still skips it, and the untruncated failure text
    is on halt_history either way. It is a convenience for the human reading the
    queue, not a load-bearing value -- which is why a heuristic is proportionate here
    and would not be for a classification decision."""
    sources = [detail or ""]
    for name, keys in (("decision.yaml", ("rationale", "blocking_issues")),
                       ("escalation_request.yaml", ("reason", "detail", "component"))):
        path = run_dir / "artifacts" / name
        if not path.exists():
            continue
        doc = orch.load_yaml(path) or {}
        for key in keys:
            value = doc.get(key)
            if isinstance(value, str):
                sources.append(value)
            elif isinstance(value, list):
                sources.extend(str(v) for v in value)
    for text in sources:
        match = _COMPONENT_NAME_RE.search(text)
        if match:
            return match.group(1)
    return "unnamed"


def _run_has_trial_row(run_id: str) -> bool:
    """Whether campaign_state.trial_sharpes already holds a row for this run --
    MEASURED, not inferred from which stage the reason implies. Feeds the
    quarantine record's `no_data_touched` (R7's fourth bullet: the absence of a
    trial row must be a recorded decision, not a gap someone re-derives later)."""
    campaign = orch.load_campaign_state()
    return any(t.get("trial_id") == run_id for t in campaign.get("trial_sharpes", []) or [])


def _apply_trial_accounting(reason: str, run_id: str, detail: str) -> str:
    """R7. CALLS the existing machinery in run_phase1_research; never reimplements it
    and never adds a new trial-recording function. Returns a one-line disposition for
    the quarantine record.

    - component_execution_error -> orch._mark_trial_invalidated. F6's own text is
      binding here (run_phase1_research.determine_post_verdict_route's F6 branch):
      "Fix the component/config, then re-run fresh. No trial or parameter-dimension
      slot is consumed; no family is marked failed." Any row already written is
      marked invalid, never deleted -- run_059 (halts #13/#14) carries both a
      prescreen and a backtest row, so there is generally something to mark.
    - no_signal_artifact -> nothing. The A6.2 prescreen row is already written
      upstream, in run_tool_worker's signal_prescreen branch
      (`_record_prescreen_trial(run_id, ps, config_path, upsert=True)`), which runs
      BEFORE determine_post_prescreen_route reads the same prescreen_result.yaml and
      takes the F5c branch. Confirmed live as well as in code: run_054's row reads
      route=no_signal_artifact, statistic_valid=neither.
    - component_gap -> nothing, and no row exists yet. component_gap is decided in
      determine_post_spec_route, i.e. at `backtest_specification`, which stages.yaml [ARCHIVED 2026-08-24 -> E-033/artifacts/]
      places strictly BEFORE `signal_prescreen` -- the first stage that records a
      trial at all. Nothing has touched market data.
    - new_component_escalation -> nothing, but for the OPPOSITE reason, and this
      corrects a premise: it does NOT fire before any backtest. _route_escalate is
      reached only from determine_post_verdict_route / determine_post_campaign_review_
      route, both of which require verdict_interpretation.yaml, which requires
      protocol_execution to have run. So a trial row generally DOES exist -- and it
      must be left alone. It is a real measurement of a real run whose hypothesis
      then routed to "the engine needs a new piece"; that is a research routing
      decision, not an engineering failure of the measurement, so invalidating it
      would under-count N in the anti-conservative direction. `no_data_touched` on
      the quarantine record is therefore measured per-run (_run_has_trial_row), never
      assumed from the reason code.
    """
    if reason == "component_execution_error":
        marked = orch._mark_trial_invalidated(
            run_id, f"E-030 S2a quarantine: {reason}"
                    f"{' — ' + detail if detail else ''}")
        return ("marked_trial_invalidated" if marked
                else "no_trial_row_to_invalidate")
    if reason == "no_signal_artifact":
        return "prescreen_row_already_recorded_by_a6_2_upstream"
    return "no_action_required"


# ---------------------------------------------------------------------------
# Resuming a halted campaign after a human fix
# ---------------------------------------------------------------------------

def resume_paused_entry(queue: dict) -> bool:
    """Called for --resume. Verifies the human has actually resolved the
    pause before flipping the queue entry back to in_progress. For the
    data_block_hitl pause specifically, invokes orch.resume_pipeline()
    directly (its own hardcoded resume path); every other pause type just
    needs the queue entry unlocked so the normal loop calls run_loop() again,
    which continues from pipeline_state.yaml's own pending_stage.

    Slice 6c S2c: a parked entry (paused:waiting_for_*) is never taken by
    --resume -- it is not a campaign stop, and taking it first would refuse
    the real pause behind it. --unpark (_unpark_entry) restores one."""
    paused = [e for e in queue["queue"] if str(e.get("status", "")).startswith("paused:")
              and not str(e.get("status", "")).startswith(PARKED_STATUS_PREFIX)]
    if not paused:
        print("No paused queue entry found — nothing to resume.")
        parked = [e["id"] for e in queue["queue"]
                  if str(e.get("status", "")).startswith(PARKED_STATUS_PREFIX)]
        if parked:
            print(f"Parked entries ({parked}) are not resumed by --resume: build the component "
                  f"or fetch the data, then --unpark <entry_id> (RUNBOOK.md §4).")
        return False
    entry = paused[0]
    if entry["status"] == f"paused:{FLAG_PREFLIGHT_HALT}":
        # E-061 C1.5: config-level, so the config itself says whether it is
        # resolved. A fresh entry refused before setup_run has no run: back to
        # ready. One with a run continues below (its status was not touched).
        refusal = _flag_preflight_refusal()
        if refusal:
            print(f"--resume refused for {entry['id']}: the flag pre-flight still refuses: "
                  f"{refusal}. Fix config/campaign_config.yaml (RUNBOOK.md §3, "
                  f"'{FLAG_PREFLIGHT_HALT}' row), then retry --resume.")
            return False
        if not entry.get("run_ids"):
            entry["status"] = "ready"
            _save_queue(queue)
            _log(f"RESUME {entry['id']}: flag pre-flight passes; no run was created, so the "
                 f"entry is ready again.")
            return True
    if entry["status"] == f"paused:{LAUNCH_EXCEPTION_HALT}":
        # E-061 (third-round review fix 5): the failed launch is recorded on the
        # entry (launch_failed_run_id, launch_exception_detail), never in
        # run_ids, and its run dir is marked abandoned_launch. The entry was put
        # back as it was before the launch, so --resume relaunches it with the
        # status it had then (launch_prior_status, fourth-round review fix 4 --
        # never a second in_progress lineage); an entry recorded before that
        # field existed falls back to ready / in_progress by whether it has runs.
        # Fix the cause first -- the same failure pauses it again.
        failed = entry.pop("launch_failed_run_id", None)
        entry.pop("launch_exception_detail", None)
        prior = entry.pop("launch_prior_status", None)
        entry["status"] = prior or ("in_progress" if entry.get("run_ids") else "ready")
        _save_queue(queue)
        _log(f"RESUME {entry['id']}: launch_exception -- relaunching as {entry['status']} "
             f"(the failed launch {failed or '(no run id allocated)'} stays "
             f"{ABANDONED_LAUNCH_STATUS}).")
        return True
    if not entry.get("run_ids"):
        print(f"Queue entry {entry['id']} is marked paused but has no run_ids — inconsistent state.")
        return False
    run_id = entry["run_ids"][-1]
    run_dir = ROOT / "runs" / run_id
    reason = entry["status"].split(":", 1)[1] if ":" in entry["status"] else ""

    if reason == "data_block_hitl":
        state = orch.load_yaml(run_dir / "pipeline_state.yaml")
        if state.get("status") != "paused_for_human":
            print(f"{run_id}: status is {state.get('status')!r}, expected 'paused_for_human' "
                  f"for a data_block_hitl resume.")
            return False
        resolution_path = run_dir / "artifacts" / "human_resolution.yaml"
        if not resolution_path.exists():
            print(f"Missing {resolution_path} — write it first (status: resolved_proceed or "
                  f"unresolvable), per RUNBOOK.md, then retry --resume.")
            return False
        # E-061 review fix 4 (+ third-round fixes 3-4): resume_pipeline goes
        # straight into run_loop. The resolution is read FIRST: anything but
        # resolved_proceed only closes the run (resume_pipeline marks it
        # rejected), so no pre-flight or regeneration applies. resolved_proceed
        # runs the same pre-flights as process_once (and a pre-spend protocol
        # regeneration) before anything is resumed: a refusal -- or an exception
        # in them -- leaves the entry paused:data_block_hitl so --resume can still
        # complete the resolution. An exception from resume_pipeline itself is a
        # classified stage_exception pause, never a raw traceback with the entry
        # left in_progress.
        # Fourth-round review fixes 7-8: the flag values are read for every
        # resolution (a non-proceed resume still writes schedulability.yaml if
        # it ends in a pause), and the resolution file itself is parsed inside
        # the classified handling -- a malformed one is refused like any other
        # pre-flight failure, the entry staying paused:data_block_hitl.
        flag_values, flag_refusal = _flag_preflight()
        try:
            resolution = orch.load_yaml(resolution_path)
            if not isinstance(resolution, dict):
                raise ValueError(f"{resolution_path.name} is not a mapping "
                                 f"(got {type(resolution).__name__})")
            refusal = None
            if resolution.get("status") == "resolved_proceed":
                if flag_refusal is not None:
                    refusal = f"{FLAG_PREFLIGHT_HALT}: {flag_refusal}"
                else:
                    refusal, regeneration = _protocol_preflight(
                        run_dir, run_id, ignore_pending=True,
                        promotion_retired=_promotion_retired_from(flag_values, flag_refusal))
                    if refusal is not None:
                        refusal = f"{PROTOCOL_PREFLIGHT_HALT}: {refusal}"
                    elif regeneration is not None:
                        _regenerate_protocol(run_id, regeneration)
        except Exception as exc:
            traceback.print_exc()
            detail = (f"the data_block_hitl --resume pre-flight raised "
                      f"{type(exc).__name__}: {exc}")
            try:
                orch.update_state(path=run_dir, last_error=detail)
                _append_halt_history(run_dir, orch.load_yaml(run_dir / "pipeline_state.yaml")
                                     or {}, "data_block_hitl", detail)
            except Exception as state_exc:
                detail += (f" [{run_id}: pipeline_state.yaml could not be updated "
                           f"({type(state_exc).__name__}: {state_exc})]")
            print(f"--resume refused for {entry['id']} / {run_id}: {detail}. See RUNBOOK.md "
                  f"§3; fix it, then retry --resume.")
            _log(f"RESUME REFUSED {entry['id']} / {run_id} (data_block_hitl): {detail}")
            _log(f"HALT — data_block_hitl: {detail}. {entry['id']} / {run_id} stays "
                 f"paused:data_block_hitl; fix it and retry --resume. See RUNBOOK.md §3.")
            return False
        if refusal:
            print(f"--resume refused for {entry['id']} / {run_id} before resume_pipeline: "
                  f"{refusal}. See RUNBOOK.md §3; fix it, then retry --resume.")
            _log(f"RESUME REFUSED {entry['id']} / {run_id} (data_block_hitl): {refusal}")
            return False
        _clear_run_halt_flags(run_dir)
        entry["status"] = "in_progress"
        _save_queue(queue)
        _log(f"RESUME {entry['id']} / {run_id}: data_block_hitl — invoking resume_pipeline().")
        try:
            orch.resume_pipeline(run_id)
        except Exception as exc:
            traceback.print_exc()
            _halt_run(queue, entry, run_id, run_dir, STAGE_EXCEPTION_HALT,
                      f"{type(exc).__name__}: {exc}",
                      flag_values.get("schedulability_block") is True)
            return False
        return True

    if reason in (LEGACY_CONTINUATION_HALT, REFINEMENT_BRIEF_HALT, IDEA_STATUS_HALT, REFRAME_HALT):
        # Slice 6c S2a: the run is not paused for these halts, so its status
        # cannot say whether they are resolved; the halt's own condition does.
        blocker = _retired_routing_halt_blocker(entry, reason)
        if blocker:
            print(f"{entry['id']} is still blocked ({reason}): {blocker}. Resolve it first "
                  f"(see RUNBOOK.md §3), then retry --resume.")
            return False
    state = orch.load_yaml(run_dir / "pipeline_state.yaml")
    still_stuck = (
        state.get("status") in ("paused_for_human", "failed")
        or (state.get("pending_stage") or "") == "human_pause"
    )
    if still_stuck:
        print(f"{run_id} still shows status={state.get('status')!r}, "
              f"pending_stage={state.get('pending_stage')!r}. Resolve the '{reason}' pause "
              f"first (see RUNBOOK.md), then retry --resume.")
        return False
    if (reason in ("profit_bars_reached", orch.HOLDOUT_UNLOCK_REFUSED_FLAG)
            and orch._verdict_routing_retired_enabled()):
        # Slice 6c S2d: resuming from the branch-3 stop needs a valid operator
        # holdout_decision.yaml (spend or continue) -- refused here, loudly,
        # before anything runs; run_loop checks it again, authoritatively.
        blocker = orch.holdout_decision_resume_blocker(run_dir, run_id)
        if blocker:
            print(f"--resume refused for {entry['id']} / {run_id}: {blocker}. Write or fix "
                  f"runs/{run_id}/artifacts/{orch.HOLDOUT_DECISION_FILE} (RUNBOOK.md §3, "
                  f"'{reason}' row), then retry --resume.")
            return False
    _clear_run_halt_flags(run_dir)
    entry["status"] = "in_progress"
    _save_queue(queue)
    _log(f"RESUME {entry['id']} / {run_id}: resolution confirmed for '{reason}', "
         f"resuming queue processing.")
    return True


def _clear_run_halt_flags(run_dir: Path) -> None:
    """E-061 review fix 1 (+ fourth-round fix 2): every un-pause path -- --resume,
    --unpark, and resume_pipeline itself -- clears the run-level halt flags
    (stage_exception, protocol_promotion_unratified, launch_exception) the
    operator's RUNBOOK §4 reset may have left set -- update_state only merges
    flags, so a stale one would otherwise stay true for the rest of the run."""
    state_path = run_dir / "pipeline_state.yaml"
    if not state_path.exists():
        return
    stale = orch._stale_run_halt_flags(orch.load_yaml(state_path) or {})
    if stale:
        orch.update_state(path=run_dir, flags=stale)


def _unpark_entry(entry_id: str) -> bool:
    """--unpark <entry_id> (slice 6c S2c, S1_FINDINGS_6C.md guess 8), after the
    operator built the component or fetched the data. Under the campaign lock
    (the single-writer rule), refuses unless the entry is paused:waiting_for_*
    and its run carries the matching parked marker, and -- for a component park
    -- while any class the park named is still not defined. Then clears the
    marker, sets the run `status: active` at the marker's resume_stage (the same
    run continues; parking always happens before any backtest, so no trial row
    is lost), and sets the entry `ready` with its priority kept -- never
    in_progress, so there are never two active lineages. The scheduler runs it
    by its own rule; nothing is minted and decide-next is not called."""
    lock_path = campaign_lock.lock_path_for(orch.CAMPAIGN_STATE_PATH)
    try:
        campaign_lock.acquire(lock_path)
    except campaign_lock.CampaignLockHeld as exc:
        print(f"--unpark refused: {exc}")
        return False
    try:
        queue = _load_queue()  # re-read under the lock
        entry = next((e for e in queue.get("queue") or []
                      if isinstance(e, dict) and e.get("id") == entry_id), None)
        if entry is None:
            print(f"--unpark refused: no queue entry {entry_id!r}.")
            return False
        status = str(entry.get("status") or "")
        if not status.startswith(PARKED_STATUS_PREFIX):
            print(f"--unpark refused: {entry_id} is {status!r}, not parked "
                  f"({' / '.join(PARKED_STATUSES)}). A campaign pause uses --resume.")
            return False
        if not entry.get("run_ids"):
            print(f"--unpark refused: {entry_id} is parked but has no run_ids — inconsistent state.")
            return False
        run_id = entry["run_ids"][-1]
        run_dir = ROOT / "runs" / run_id
        state = _run_state(run_id)
        marker = state.get(orch.PARKED_KEY)
        kind = status[len(PARKED_STATUS_PREFIX):]
        if not isinstance(marker, dict) or marker.get("kind") != kind:
            print(f"--unpark refused: {run_id}'s pipeline_state.yaml {orch.PARKED_KEY} is "
                  f"{marker!r}, which does not match the entry's {status!r}. Inconsistent "
                  f"state: fix one of them by hand.")
            return False
        if state.get("status") != "paused_for_human":
            print(f"--unpark refused: {run_id} is status={state.get('status')!r}, expected "
                  f"'paused_for_human' for a parked run.")
            return False
        if kind == "component":
            # The one shared "is this component class defined" check (review
            # fixes 2 + 8): the same function and scope 5a parking and
            # decide_next.known_component_classes use. A definition that still
            # fails to import is caught when the run re-validates at
            # backtest_specification (and pauses or parks again).
            import decide_next as dn
            missing = [c for c in marker.get("classes") or []
                       if dn.component_class_status(_TRADING_BOT_ROOT, c) != "defined"]
            if missing:
                print(f"--unpark refused: {entry_id} waits on {missing}, still not defined under "
                      f"{_TRADING_BOT_ROOT}. Build it first (STRATEGY_EXTENDING.md).")
                return False
        resume_stage = marker.get("resume_stage") or state.get("pending_stage")
        orch.update_state(path=run_dir, status="active", pending_stage=resume_stage,
                          **{orch.PARKED_KEY: None})
        _clear_run_halt_flags(run_dir)  # E-061 fourth-round fix 2: every un-pause path
        entry["status"] = "ready"
        entry.pop("parked_reason", None)
        _save_queue(queue)
        _regenerate_summary(queue)
        _log(f"UNPARK {entry_id} / {run_id}: waiting_for_{kind} cleared by the operator; entry "
             f"ready (priority {entry.get('priority')}), the run resumes at {resume_stage}.")
        _write_loop_health()  # review fix 9: like every other status-changing branch
        if _schedulability_block_enabled():
            _write_schedulability()
        return True
    finally:
        campaign_lock.release(lock_path)


# ---------------------------------------------------------------------------
# Observability: campaign_log.md (append-only) and campaign_summary.md (regenerated)
# ---------------------------------------------------------------------------

def _log(line: str, dry_run: bool = False):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    tag = " [DRY RUN]" if dry_run else ""
    full = f"- {ts}{tag} {line}"
    print(full)
    with open(CAMPAIGN_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(full + "\n")


def _extract_run_numbers(run_dir: Path) -> dict:
    """Best-effort numeric summary for a log line — degrades gracefully when a
    run hasn't reached a stage that produces the relevant artifact yet."""
    out = {}
    artifacts = run_dir / "artifacts"

    ps_path = artifacts / "prescreen_result.yaml"
    if ps_path.exists():
        d = orch.load_yaml(ps_path) or {}
        if d.get("ic_spearman_pooled") is not None:
            out["ic"] = d["ic_spearman_pooled"]
        cc = d.get("cost_check") or {}
        if cc.get("edge_to_cost_ratio") is not None:
            out["cost_ratio"] = cc["edge_to_cost_ratio"]
        if d.get("route"):
            out["prescreen_route"] = d["route"]

    pr_path = artifacts / "protocol_result.yaml"
    if pr_path.exists():
        d = orch.load_yaml(pr_path) or {}
        hv = d.get("hypothesis_verdict") or {}
        if hv.get("verdict"):
            out["backtest_verdict"] = hv["verdict"]
        pss = d.get("per_symbol_summary") or {}
        sharpes = [v.get("median_sharpe") for v in pss.values() if v.get("median_sharpe") is not None]
        if sharpes:
            out["median_sharpe"] = round(sum(sharpes) / len(sharpes), 3)

    vi_path = artifacts / "verdict_interpretation.yaml"
    if vi_path.exists():
        d = orch.load_yaml(vi_path) or {}
        v = d.get("status") or d.get("protocol_verdict")
        if v:
            out["verdict_status"] = v

    # E-046a Slice 5b-ii-B: under orchestrator.specialist_readers.enabled no
    # verdict_interpretation.yaml is written; the grid's idea_status is the
    # run's decision, so the log line shows that instead. Flag off: untouched.
    is_path = artifacts / "idea_status.yaml"
    try:
        _sr_on = orch._specialist_readers_enabled()
    except ValueError:
        _sr_on = False  # best-effort log line: a misconfigured flag fails run_loop, not this
    if _sr_on and is_path.exists():
        # Slice 6c S2a code review (item 5): best-effort like the flag read above --
        # an unreadable idea_status.yaml must reach process_once's integrity halt
        # (idea_status_missing_at_done), not crash this log line first.
        try:
            d = orch.load_yaml(is_path) or {}
        except Exception:
            d = {}
        if isinstance(d, dict) and d.get("idea_status"):
            out["idea_status"] = d["idea_status"]

    return out


def _log_transition(entry: dict, run_id: str, state: dict, dry_run: bool = False):
    pending = state.get("pending_stage", "?")
    status = state.get("status", "?")
    numbers = _extract_run_numbers(ROOT / "runs" / run_id)
    numbers_str = ", ".join(f"{k}={v}" for k, v in numbers.items()) if numbers else "no scored artifacts yet"
    _log(f"STAGE  {entry['id']} / {run_id}: pending_stage={pending} status={status} ({numbers_str})", dry_run)


# ---------------------------------------------------------------------------
# One-hypothesis-per-run split handling (architecture rule, 2026-07-06)
#
# hypothesis_generation producing multiple hypothesis_card_*.yaml files (e.g. a
# reframe whose research_goal named more than one mechanism) is handled at the
# orchestrator level (run_phase1_research._handle_hypothesis_generation_multi_card_split):
# the parent run keeps the first card and proceeds normally; every additional card
# gets its own freshly-scaffolded sibling run, already past hypothesis_generation,
# recorded in campaign_state.yaml's hypothesis_splits. This wrapper's job is just to
# give each sibling its OWN queue entry — unlike a reframe/escalate continuation
# (same brief lineage, appended to the SAME entry's run_ids), a split is a genuinely
# distinct hypothesis that happens to share an ancestor.
# ---------------------------------------------------------------------------

def _snapshot_hypothesis_splits() -> list:
    campaign = orch.load_campaign_state()
    return list(campaign.get("hypothesis_splits") or [])


def _add_queue_entry_for_split_child(queue: dict, parent_entry: dict, parent_run_id: str, child_id: str):
    new_id = f"{parent_entry['id']}__split_{child_id}"
    queue["queue"].append({
        "id": new_id,
        "brief_path": parent_entry.get("brief_path"),
        "status": "in_progress",
        "priority": parent_entry.get("priority", 999),
        "notes": (
            f"Split off {parent_run_id}'s multi-card hypothesis_generation output "
            f"(architecture rule: one hypothesis per run — see "
            f"campaign_state.yaml hypothesis_splits for the parent linkage). "
            f"{child_id}'s pipeline_state.yaml already carries hypothesis_card.yaml "
            f"and is past hypothesis_generation."
        ),
        "run_ids": [child_id],
        "outcome": None,
    })


def _total_campaign_spend() -> tuple:
    total_weighted = 0.0
    total_usd = 0.0
    runs_dir = ROOT / "runs"
    if not runs_dir.exists():
        return total_weighted, total_usd
    for run_dir in runs_dir.iterdir():
        if not run_dir.is_dir() or run_dir.name.startswith("run_dryrun"):
            continue
        ps_path = run_dir / "pipeline_state.yaml"
        if not ps_path.exists():
            continue
        try:
            state = orch.load_yaml(ps_path) or {}
        except Exception:
            continue
        for stage_entry in (state.get("audit_log") or {}).values():
            tokens = stage_entry.get("tokens") or {}
            total_weighted += tokens.get("weighted", 0) or 0
            total_usd += stage_entry.get("cost_usd", 0) or 0
    return total_weighted, total_usd


def _regenerate_summary(queue: dict, dry_run: bool = False):
    campaign = orch.load_campaign_state()
    trials = campaign.get("trial_sharpes", [])
    outcomes = {}
    for t in trials:
        key = t.get("route") or "recorded"
        outcomes[key] = outcomes.get(key, 0) + 1
    failed_families = campaign.get("failed_families", [])
    n_failed_families = len({(f.get("name") if isinstance(f, dict) else f) for f in failed_families})

    kb_path = ROOT / "campaign_record" / "campaign_knowledge_base.yaml"
    kb_findings = 0
    if kb_path.exists():
        kb = orch.load_yaml(kb_path) or {}
        kb_findings = len(kb.get("findings", []) or [])

    total_weighted, total_usd = _total_campaign_spend()

    lines = [
        "# Campaign summary",
        "",
        f"_Regenerated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
        f"{' [DRY RUN]' if dry_run else ''}_",
        "",
        "## Queue",
        "",
        "| id | status | run_ids | outcome |",
        "|---|---|---|---|",
    ]
    for e in queue["queue"]:
        run_ids_str = ", ".join(e.get("run_ids", [])) or "-"
        # E-059 S2b: a legacy brief's one-time "[obsolete] ..." title is shown
        # next to its id; entries without a title render exactly as before.
        id_cell = f"{e['id']} ({e['title']})" if e.get("title") else e["id"]
        lines.append(f"| {id_cell} | {e['status']} | {run_ids_str} | {e.get('outcome') or '-'} |")
    # Slice 6c S2c (card J: "surfaced in the campaign summary"). Only when an
    # entry is parked, so a summary without one is unchanged.
    parked = [e for e in queue["queue"]
              if str(e.get("status", "")).startswith(PARKED_STATUS_PREFIX)]
    if parked:
        lines += ["", "## Parked (waiting for a component or data; unpark with --unpark <id>)", "",
                  "| id | status | run | waiting on | requests |", "|---|---|---|---|---|"]
        for e in parked:
            run_id = (e.get("run_ids") or ["-"])[-1]
            marker = _run_state(run_id).get(orch.PARKED_KEY) if run_id != "-" else None
            marker = marker if isinstance(marker, dict) else {}
            refs = ", ".join(marker.get("request_refs") or []) or "-"
            why = " ".join(str(e.get("parked_reason") or "-").split()).replace("|", "/")
            lines.append(f"| {e['id']} | {e['status']} | {run_id} | {why} | {refs} |")
    lines += [
        "",
        "## Scoreboard",
        "",
        f"- Trials recorded (campaign_state.trial_sharpes): {len(trials)}",
    ]
    for k, v in sorted(outcomes.items()):
        lines.append(f"  - {k}: {v}")
    lines += [
        f"- Distinct failed hypothesis families: {n_failed_families}",
        f"- Knowledge-base findings on file: {kb_findings}",
        f"- Total campaign runs so far: {len(campaign.get('runs', []))}",
        f"- Estimated spend: ${total_usd:.2f} ({total_weighted:,.0f} weighted token units, "
        f"see config/campaign_config.yaml orchestrator.token_budget_per_run_weighted_units)",
        "",
    ]
    CAMPAIGN_SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# E-030 S3 — the loop-health instrument (campaign_record/loop_health.yaml)
#
# EPIC.md Done-when #2 asks for "halt count, downtime hours, downtime share of
# span, cause breakdown, and which causes were auto-recovered vs. escalated",
# emitted per campaign run / per --once step and CONSUMED BY run_campaign.py
# itself, not only read by a human (the skill's F3 instrument-shape rule: "An
# instrument only the operator reads leaves the loop as blind as before").
#
# SCOPE NOTE, because Done-when #2's literal words are "decide retry-vs-escalate":
# there is nothing to decide between today. S2b (retry) does not exist and stays
# unbuilt -- taxonomy R2 found exactly one evidenced retry-safe signature and it is
# already handled at the stage level in _invoke_agent_with_yaml_retry (A11). The
# auto-action that DOES exist is S2a's quarantine, so the decision wired up here is
# quarantine-vs-escalate, via _repeat_quarantine (R4 extended from retry to
# quarantine -- see that function). Do not read this module as having built
# retry-vs-escalate.
#
# SHAPE: re-derived from primary records on every call, never accumulated. Same
# posture as _regenerate_summary -- the file is a projection, so a corrupted or
# hand-edited copy is repaired by the next step rather than compounding. The two
# primary records are campaign_log.md (append-only, this module's own writer) and
# each run's halt_history on pipeline_state.yaml (S1.5 Piece 1).
# ---------------------------------------------------------------------------

# Same shape as artifacts/measure_halt_cost.py's own parser, deliberately: that
# script produced E-030's measured_halt_cost.txt, and a human cross-checking this
# instrument against that artifact should not have to reconcile two parsers.
_LOG_EVENT_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z (.*)$")


def _parse_campaign_log_events(path: Path) -> list:
    """[(naive-UTC datetime, text)] for every real (non-[DRY RUN]) log event.

    Dry-run lines are excluded for the same reason measure_halt_cost.py excludes
    them: dry_run_verify() writes HALT-shaped lines with zero campaign meaning, and
    counting them would inflate halt counts with rehearsals."""
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _LOG_EVENT_RE.match(line)
        if not m or "[DRY RUN]" in line:
            continue
        try:
            events.append((datetime.fromisoformat(m.group(1)), m.group(2)))
        except ValueError:
            continue
    return events


def _pair_halts_with_downtime(events: list) -> list:
    """measure_halt_cost.py's pairing algorithm, re-implemented as a function
    (that file is a flat script and is not importable).

    THE ALGORITHM, verbatim in behavior: each HALT line is paired with the NEXT
    non-[DRY RUN] log event, and the gap between them is that halt's downtime. It
    measures latency-to-a-human-noticing, which is what S1 found most of the 127h
    actually was ("12 of 14 halts were cleared with no production-code commit inside
    the halt window"). The final halt has no successor event, so its downtime is
    None -- reported as null, never as 0.0, which would flatter the total."""
    halts = []
    for i, (when, text) in enumerate(events):
        if not text.startswith("HALT"):
            continue
        reason = re.sub(r"^HALT [—-] ", "", text).split(":")[0].split(".")[0].strip()[:32]
        nxt = events[i + 1] if i + 1 < len(events) else None
        halts.append({
            "when": when,
            "reason": reason,
            "downtime_hours": ((nxt[0] - when).total_seconds() / 3600.0) if nxt else None,
        })
    return halts


def _iter_halt_histories() -> list:
    """[(run_id, halt_history list)] over every run on disk that has one."""
    runs_dir = ROOT / "runs"
    if not runs_dir.exists():
        return []
    out = []
    for run_dir in sorted(runs_dir.iterdir()):
        if not run_dir.is_dir():
            continue
        ps_path = run_dir / "pipeline_state.yaml"
        if not ps_path.exists():
            continue
        try:
            state = orch.load_yaml(ps_path) or {}
        except Exception:
            continue
        history = state.get("halt_history")
        if isinstance(history, list) and history:
            out.append((run_dir.name, [h for h in history if isinstance(h, dict)]))
    return out


def _compute_loop_health() -> dict:
    """Re-derives the whole loop-health picture from primary records. Pure read
    plus one file write; never mutates campaign state."""
    events = _parse_campaign_log_events(CAMPAIGN_LOG_PATH)
    halts = _pair_halts_with_downtime(events)

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    span_hours = ((now - events[0][0]).total_seconds() / 3600.0) if events else None

    known = sorted(h["downtime_hours"] for h in halts if h["downtime_hours"] is not None)
    downtime_hours = sum(known)
    median = known[len(known) // 2] if known else None
    # null, not 0.0, when the span is unusable. A degenerate denominator reported as
    # "0.0% of the span was halted" is the flattering direction, and this file is
    # meant to be read when the loop is unhealthy.
    share = (100.0 * downtime_hours / span_hours) if span_hours and span_hours > 0 else None

    # TWO buckets, not three. A retry-safe halt is NOT observable from this layer:
    # the one evidenced retry-safe signature (the claude_agent_sdk==0.2.82
    # `error result: success` misclassification, taxonomy #10/#12) is resolved
    # entirely inside run_phase1_research._invoke_agent_with_yaml_retry BEFORE
    # _hard_pause_reason is ever consulted, so it never reaches campaign_log.md as a
    # HALT line at all. A `retry_safe` bucket here would therefore be permanently
    # empty and would read as "retry never helps", which is the opposite of true.
    # DO NOT ADD ONE without first moving the measurement to the stage layer.
    #
    # `quarantine_safe` here means "a halt whose reason S2a's evidenced set would
    # permit quarantining" -- it is the size of the prize, not a record of action
    # taken. With the flag off (the default) every one of these still escalated;
    # `outcomes` below is what records what actually happened.
    breakdown = {"quarantine_safe": {}, "escalate": {}}
    for h in halts:
        bucket = ("quarantine_safe" if h["reason"] in _QUARANTINE_SAFE_REASONS
                  else "escalate")
        cell = breakdown[bucket].setdefault(h["reason"], {"count": 0, "downtime_hours": 0.0})
        cell["count"] += 1
        if h["downtime_hours"] is not None:
            cell["downtime_hours"] = round(cell["downtime_hours"] + h["downtime_hours"], 3)

    # DIFFERENT DENOMINATOR FROM halts.total, on purpose, and disclosed as such.
    # campaign_log.md carries a HALT line only for halts that ESCALATED -- a
    # quarantined halt emits a QUARANTINE line and the campaign keeps going. So
    # auto_recovered can never appear in halts.total. halt_history is the record
    # that spans both, which is why the outcome split is derived from it.
    histories = _iter_halt_histories()
    auto_recovered = 0
    escalated = 0
    repeat_pairs = 0
    parked = 0
    for _run_id, history in histories:
        for i, record in enumerate(history):
            if "parked" in record:
                # Slice 6c S2c: a park stopped a run, not the loop -- neither
                # auto-recovered nor escalated, and never an R4 repeat.
                parked += 1
                continue
            if "quarantine" in record:
                auto_recovered += 1
            else:
                escalated += 1
            # The R4 population, computed with the SAME predicate the decision uses
            # (_repeat_quarantine), so the instrument and the decision cannot drift.
            if _repeat_quarantine({"halt_history": history[:i]}, record.get("reason")):
                repeat_pairs += 1

    outcomes = {
        "auto_recovered": auto_recovered,
        "escalated": escalated,
        "halt_history_records": auto_recovered + escalated,
        "repeat_quarantine_escalations": repeat_pairs,
        "denominator_note": ("halt_history across every run on disk, which covers "
                             "both quarantined and escalated halts. Does not equal "
                             "halts.total."),
    }
    if parked:
        # Only when a park exists (orchestrator.verdict_routing_retired), so the
        # flag-off file is unchanged. Not in halt_history_records.
        outcomes["parked"] = parked
    return {
        "computed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": {
            "campaign_log": str(CAMPAIGN_LOG_PATH.name),
            "halt_history_runs": len(histories),
            "note": ("Re-derived from primary records on every process_once() step; "
                     "never accumulated. Safe to delete -- the next step rewrites it."),
        },
        "span_hours": round(span_hours, 2) if span_hours is not None else None,
        "halts": {
            "total": len(halts),
            "downtime_hours": round(downtime_hours, 2),
            "downtime_share_pct": round(share, 1) if share is not None else None,
            "median_downtime_hours": round(median, 2) if median is not None else None,
            "unpaired": sum(1 for h in halts if h["downtime_hours"] is None),
            "denominator_note": ("campaign_log.md HALT lines only. A quarantined halt "
                                 "writes a QUARANTINE line, not a HALT line, so it is "
                                 "NOT counted here -- see outcomes."),
        },
        "cause_breakdown": breakdown,
        "outcomes": outcomes,
        "policy": {
            "quarantine_enabled": _quarantine_enabled(),
            "quarantine_safe_reasons": sorted(_QUARANTINE_SAFE_REASONS),
            "retry_enabled": False,
            "retry_note": ("S2b is unbuilt: taxonomy R2 found one evidenced retry-safe "
                           "signature and it is already handled at the stage level in "
                           "_invoke_agent_with_yaml_retry (A11). There is no "
                           "retry-vs-escalate decision to make at this layer."),
        },
    }


def _write_loop_health() -> dict:
    """Computes and writes campaign_record/loop_health.yaml. Returns the block.

    ROOT is resolved at CALL time rather than baked into a module constant, matching
    _regenerate_summary's own `kb_path` and _quarantine_enabled: the test sandbox
    monkeypatches ROOT, and a module constant would send every existing
    process_once() test's write into the real repository."""
    path = ROOT / "campaign_record" / "loop_health.yaml"
    block = _compute_loop_health()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(block, sort_keys=False, allow_unicode=True),
                    encoding="utf-8")
    return block


# ---------------------------------------------------------------------------
# E-031 S2 -- the schedulability block (campaign_record/schedulability.yaml)
#
# EPIC.md Done-when #2: "A schedulability block is written BEFORE the
# exhaustion return on every process_once() step: ready / in_progress /
# blocked counts, days since last completion, per-blocked-entry dwell time
# and blocker string. Consumed by run_campaign.py's own refill-vs-escalate
# decision, not only read by a human."
#
# THE BLIND SPOT THIS CLOSES (measured, not asserted): all four of E-030's
# _write_loop_health() call sites sit strictly AFTER _select_entry() returns
# a non-None entry (S1's own Task 2 finding, confirmed again here by reading
# process_once() directly). The queue-exhausted `entry is None` branch --
# the ONE condition that actually stopped the loop on 2026-07-19 -- has never
# produced any instrument at all. This is a DIFFERENT block from
# loop_health.yaml (that one is about HALTS; this one is about SCHEDULABILITY)
# and is written unconditionally near the top of process_once(), before
# _select_entry's result is even inspected, so it runs on every path.
# ---------------------------------------------------------------------------

def _schedulability_block_enabled(cfg: dict | None = None) -> bool:
    """E-031 S2 gate. False (no file written, no behavior change) when the
    key, the section, or the config file is absent -- same silence-is-never-
    a-green-light rule as _quarantine_enabled() just above. `cfg`: the parsed
    config, when the caller (the E-061 launch pre-flight) already has it."""
    if cfg is None:
        path = ROOT / "config" / "campaign_config.yaml"
        if not path.exists():
            return False
        with open(path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    # E-061 C1.5: strict, the one check every orchestrator.<name>.enabled reader uses.
    return orch._strict_orchestrator_flag("schedulability_block", cfg=cfg)


# Statuses that are NOT "blocked" for schedulability purposes. `ready` and
# `in_progress` are schedulable; `done` and `superseded` are TERMINAL (both are
# schema-legal per _QUEUE_STATUS_RE). Review fix 2, 2026-08-26: `superseded`
# was previously bucketed as blocked, emitting a phantom blocker row.
# E-059 S2a: `queued` (an agent candidate waiting, never auto-picked) is not
# blocked either -- S1_FINDINGS_6B.md guess 5.
_SCHEDULABILITY_NON_BLOCKED_STATUSES = ("ready", "in_progress", "done", "superseded", "queued")

# An entry id is followed in the log by one of these, or by end-of-line. NOT a
# bare `in` test -- see _mentions_entry_id.
_ID_BOUNDARY_RE = re.compile(r"[A-Za-z0-9_-]")


def _mentions_entry_id(text: str, entry_id: str) -> bool:
    """Whole-token match for a queue entry id inside a campaign_log.md line.

    Review fix 1 (2026-08-26), HIGH severity, reproduced before fixing: the
    previous test was a bare `entry_id in text`. `_add_queue_entry_for_split_
    child` mints child ids as f"{parent_id}__split_{child_id}", so a parent's
    id is ALWAYS a substring of every one of its split children's ids. Any
    activity on a split child therefore reset the blocked PARENT's dwell_days
    to ~0 -- e.g. `P4_ts_trend` blocked 40 days reported dwell_days: 0.0 given
    a 5-minute-old `LAUNCH P4_ts_trend__split_run_071` line.

    That is exactly the flattering direction _compute_schedulability's own
    docstring forbids ("an unknown dwell time must never read as 'just now'"),
    and it silently defeats the escalate-vs-refill consumer this block exists
    to feed: the longest-blocked entry reads as the freshest.

    Fixed by requiring the character following the id to not continue the
    identifier (so `P4_ts_trend__split_x` no longer matches `P4_ts_trend`,
    while `LAUNCH P4_ts_trend -> run_054` still does)."""
    if not entry_id:
        return False
    start = 0
    while True:
        idx = text.find(entry_id, start)
        if idx == -1:
            return False
        after = idx + len(entry_id)
        if after >= len(text) or not _ID_BOUNDARY_RE.match(text[after]):
            return True
        start = after


def _blocker_of(status):
    """The blocker itself, not the raw status string.

    Review fix 4 (2026-08-26): `blocker` was a verbatim copy of `status`, so
    the field advertised as a "blocker string" carried zero information beyond
    it -- a consumer still had to re-parse the `blocked_on_` / `paused:`
    prefix, which is the parse this field exists to spare it."""
    if not isinstance(status, str):
        return None
    if status.startswith("blocked_on_"):
        return status[len("blocked_on_"):]
    if status.startswith("paused:"):
        return status[len("paused:"):]
    return status


def _compute_schedulability() -> dict:
    """Re-derives the whole schedulability picture from primary records
    (campaign_queue.yaml + campaign_log.md). Pure read, no file write --
    same split as _compute_loop_health/_write_loop_health, so a caller that
    wants to ADD a field (e.g. S3's refill_scan) can do so before the one
    write actually happens.

    dwell_days is derived from the last campaign_log.md line that mentions
    a blocked entry's own id -- the queue entry schema
    (tools/record_schema.py's QUEUE_ENTRY_SCHEMA) has no per-entry timestamp
    field, so campaign_log.md (this module's own append-only writer) is the
    only primary record that can answer "how long has this been blocked."
    None (not 0) when no mention is found -- an unknown dwell time must
    never read as "just now," which would be the flattering direction."""
    queue = _load_queue()
    entries = queue.get("queue") or []

    ready = [e for e in entries if e.get("status") == "ready"]
    in_progress = [e for e in entries if e.get("status") == "in_progress"]
    done = [e for e in entries if e.get("status") == "done"]
    # Review fix 2 (2026-08-26): `superseded` is a schema-legal TERMINAL queue
    # status (_QUEUE_STATUS_RE, tools/record_schema.py) -- retired, not
    # blocked. Counting it as blocked emitted a phantom blocked_entries row
    # with blocker: "superseded" and a dwell time, inflating the very backlog
    # S3's escalate decision is meant to key on.
    blocked = [e for e in entries
               if e.get("status") not in _SCHEDULABILITY_NON_BLOCKED_STATUSES]

    events = _parse_campaign_log_events(CAMPAIGN_LOG_PATH)
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Review fix 5 (2026-08-26): the quarantine path also COMPLETES an entry
    # (status="done" + outcome set) but logs "QUARANTINE", not "DONE". Counting
    # only DONE made a loop that advances via quarantine read as permanently
    # stalled, contradicting counts.done in the same block. Both are
    # completions; last_completion_basis names which kind was found.
    last_completion_at = None
    last_completion_kind = None
    for when, text in reversed(events):
        if text.startswith("DONE "):
            last_completion_at, last_completion_kind = when, "DONE"
            break
        if text.startswith("QUARANTINE"):
            last_completion_at, last_completion_kind = when, "QUARANTINE"
            break
    days_since_last_completion = (
        round((now - last_completion_at).total_seconds() / 86400.0, 2)
        if last_completion_at is not None else None
    )

    blocked_entries = []
    for e in blocked:
        eid = e.get("id")
        last_mention = None
        for when, text in reversed(events):
            if eid and _mentions_entry_id(text, eid):
                last_mention = when
                break
        blocked_entries.append({
            "id": eid,
            "status": e.get("status"),
            "blocker": _blocker_of(e.get("status")),
            "dwell_days": (round((now - last_mention).total_seconds() / 86400.0, 2)
                           if last_mention is not None else None),
            "dwell_basis": ("last campaign_log.md mention of this entry id"
                            if last_mention is not None else
                            "no campaign_log.md mention found for this id -- "
                            "dwell time unknown, not zero"),
        })

    return {
        "computed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": {
            "campaign_queue": str(QUEUE_PATH.name),
            "campaign_log": str(CAMPAIGN_LOG_PATH.name),
            "note": ("Re-derived from primary records on every process_once() "
                     "step; never accumulated. Safe to delete -- the next "
                     "step rewrites it."),
        },
        "counts": {
            "total": len(entries),
            "ready": len(ready),
            "in_progress": len(in_progress),
            "done": len(done),
            "blocked": len(blocked),
        },
        "days_since_last_completion": days_since_last_completion,
        "last_completion_basis": (
            f"last campaign_log.md {last_completion_kind} line"
            if last_completion_at is not None
            else "no DONE or QUARANTINE line found in campaign_log.md"),
        "blocked_entries": blocked_entries,
    }


def _write_schedulability_block(block: dict) -> dict:
    path = ROOT / "campaign_record" / "schedulability.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(block, sort_keys=False, allow_unicode=True),
                    encoding="utf-8")
    return block


def _write_schedulability() -> dict:
    """Computes and writes campaign_record/schedulability.yaml in one call --
    the convenience wrapper process_once() uses on its own unconditional,
    every-step write. S3's refill path calls _compute_schedulability() and
    _write_schedulability_block() separately so it can attach refill_scan
    before the (second, final-for-this-step) write."""
    return _write_schedulability_block(_compute_schedulability())



# ---------------------------------------------------------------------------
# Main queue-processing loop
# ---------------------------------------------------------------------------

def _snapshot_run_dirs() -> set:
    runs_dir = ROOT / "runs"
    if not runs_dir.exists():
        return set()
    return {p.name for p in runs_dir.iterdir() if p.is_dir()}


# ---------------------------------------------------------------------------
# A3 (K4 kernel): scaffold/registration reconciler. See design note section 6.
# ---------------------------------------------------------------------------

def _referenced_run_ids() -> set:
    """Every run_id counted as 'registered' by ANY of: campaign_queue.yaml's
    run_ids, campaign_state.yaml's runs/trial_sharpes/hypothesis_splits, or
    the frozen baseline file. trial_sharpes and hypothesis_splits are
    included deliberately -- run_041/run_042 (design note section 4) are
    referenced ONLY via trial_sharpes, never campaign_state.runs; omitting
    either surface would make the reconciler false-positive on them."""
    referenced = set()
    queue = _load_queue()
    for e in queue.get("queue", []):
        referenced.update(e.get("run_ids") or [])
    campaign = orch.load_campaign_state()
    referenced.update(campaign.get("runs", []))
    referenced.update(t["trial_id"] for t in campaign.get("trial_sharpes", [])
                       if t.get("trial_id"))
    for ev in campaign.get("hypothesis_splits") or []:
        if ev.get("parent_run"):
            referenced.add(ev["parent_run"])
        referenced.update(ev.get("children") or [])
    if BASELINE_PATH.exists():
        baseline = orch.load_yaml(BASELINE_PATH) or {}
        referenced.update(r["id"] for r in baseline.get("grandfathered_runs", []) if r.get("id"))
    return referenced


def _is_quarantined_orphan(run_id: str) -> bool:
    """Hand-set convention (run_055/run_056 precedent): an ORPHANED_README.md
    in the run's own directory. A3 leaves A4's later work (a first-class
    quarantined_orphan STATUS field recognized by selectors) as a separate,
    later ledger item -- this is only the detection half.

    E-061 C1.4 (third-round review fix 6): a run dir a failed launch left behind
    (pipeline_state.yaml status: abandoned_launch, see _mark_abandoned_launch)
    is known the same way -- recorded, never reported as unexpected."""
    if (ROOT / "runs" / run_id / "ORPHANED_README.md").exists():
        return True
    return abandoned_launch.is_abandoned_launch(ROOT / "runs" / run_id)


def reconcile_orphans() -> list:
    """Read-only. Returns the full sorted list of runs/ directories
    referenced by none of campaign_queue.yaml / campaign_state.yaml /
    the frozen baseline (quarantined and unexpected alike).

    Always emits EXACTLY ONE log line per invocation (K4 rider,
    2026-07-13): a clean pass (zero unexpected orphans) used to log
    nothing at all, making it indistinguishable from reconcile_orphans()
    never having run. Non-clean case logs the UNEXPECTED subset (not
    already known-quarantined), content unchanged from before this rider,
    so a real crash-window orphan (A1/A3's crash-window analysis) is never
    silently missed, while the already-known run_055/run_056-style orphans
    don't spam that line's content on every invocation -- they still count
    toward the clean-case line's coverage numbers instead. Never blocks
    _select_entry()/_next_new_run_id() -- both already scan runs/ on disk
    directly and independently exclude every occupied number regardless
    of this function's output."""
    on_disk = _snapshot_run_dirs()
    referenced = _referenced_run_ids()
    orphans = sorted(on_disk - referenced)
    unexpected = [o for o in orphans if not _is_quarantined_orphan(o)]
    if unexpected:
        _log(f"RECONCILE: {len(unexpected)} unreferenced run dir(s) not in "
             f"campaign_queue.yaml/campaign_state.yaml/{BASELINE_PATH.name}: {unexpected}")
    else:
        covered = len(on_disk) - len(orphans)
        _log(f"RECONCILE: {len(on_disk)} run dir(s) scanned, {covered} "
             f"referenced/grandfathered, 0 unexpected ({len(orphans)} known-quarantined)")
    return orphans


# ---------------------------------------------------------------------------
# E-061 C1.4 / C1.5 -- the launch pre-flight and the stage-exception pause
# (delivery_plan_v26_continuation.md C1; review_2026-09-27/DELIVERY_REVIEW.md
# A4, A6, A8; A3_all_flags_on.md §1 and §3.3). Every refusal here is a
# classified pause (paused:<reason>, a HALT line naming the culprit, a
# halt_history record when a run exists) and process_once returns False: the
# campaign process never crashes into a restart loop, and nothing is spent.
# ---------------------------------------------------------------------------

def _flag_readers() -> dict:
    """{flag name: its reader}, looked up at call time. The launch pre-flight
    calls EVERY one of them, on one parsed config (third-round review fix 10:
    the readers are the single source of the rules -- no copy of them here)."""
    return {
        "exclusion_digest_input": orch._exclusion_digest_input_enabled,
        "stale_input_path_fix": orch._stale_input_path_fix_enabled,
        "variant_selection_record": orch._variant_selection_record_enabled,
        "data_availability_gate": orch._data_availability_gate_enabled,
        "grid_evaluation": orch._grid_evaluation_enabled,
        "category_reports": orch._category_reports_enabled,
        "profit_bars_file": orch._profit_bars_file_enabled,
        "config_direct_authoring": orch._config_direct_authoring_enabled,
        "variant_loop": orch._variant_loop_enabled,
        "specialist_readers": orch._specialist_readers_enabled,
        "regroup_record": orch._regroup_record_enabled,
        "score_provenance": orch._score_provenance_enabled,  # C5.7b-1
        "profit_bars_every_backtest": orch._profit_bars_every_backtest_enabled,
        "profit_bars_v2": orch._profit_bars_v2_enabled,  # E-062 S2b-1
        "decide_next": orch._decide_next_enabled,
        "verdict_routing_retired": orch._verdict_routing_retired_enabled,
        "composition_runs": orch._composition_runs_enabled,
        "variant_anti_adjacency_gate": orch._variant_anti_adjacency_gate_enabled,
        "forecast_size_probe": orch._forecast_size_probe_enabled,  # D-056
        "schedulability_block": _schedulability_block_enabled,
    }


def _flag_preflight() -> tuple:
    """(values, refusal): config/campaign_config.yaml parsed ONCE and handed to
    every real flag reader (_flag_readers), before anything launches, on every
    step. `values` holds each flag whose reader returned (so a valid
    schedulability_block still reads true while another flag is refused);
    `refusal` names every problem, or is None.

      (b) every orchestrator.<name>.enabled -- and halt_policy.quarantine_enabled
          -- is a real YAML bool; a quoted "false" or a null is refused;
      (a) every flag dependency holds, including the two the readers used to
          raise only after spend (A3 §1): variant_loop -> config_direct_authoring
          (first read at 5a), composition_runs -> its four prerequisites (first
          read after 1a); plus variant_anti_adjacency_gate's two, which its call
          sites check only at 5a -- regroup_record while campaign_memory.yaml
          does not exist (_repeat_gate_context), and variant_selection_record on
          the legacy, non-config-direct path (_route_post_variant_selection).
    Any other failure reading the config is a refusal too, never a crash."""
    path = ROOT / "config" / "campaign_config.yaml"
    try:
        cfg = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.exists() else {}
        if not isinstance(cfg, dict) or not isinstance(cfg.get("orchestrator") or {}, dict):
            return {}, "config/campaign_config.yaml's orchestrator: section is not a mapping"
    except Exception as e:  # a refusal, never a crash (KeyboardInterrupt passes)
        return {}, f"config/campaign_config.yaml could not be read: {type(e).__name__}: {e}"
    orch_cfg = cfg.get("orchestrator") or {}
    readers = _flag_readers()
    values, problems = {}, []

    def _note(text):
        if text not in problems:
            problems.append(text)
    # Fourth-round review fix 6: a flag section that is not a mapping (e.g.
    # `data_availability_gate: false`) would read as absent -- its default --
    # through every reader's `(section or {})`. Refused, named.
    for name in list(readers) + ["halt_policy"]:
        section = orch_cfg.get(name)
        if section is not None and not isinstance(section, dict):
            key = "quarantine_enabled" if name == "halt_policy" else "enabled"
            _note(f"orchestrator.{name} is not a mapping (got {type(section).__name__} "
                  f"{section!r}) -- write `{name}: {{{key}: true}}` or `{{{key}: false}}` "
                  f"in config/campaign_config.yaml")
    for name, reader in readers.items():
        try:
            values[name] = reader(cfg)
        except ValueError as e:
            _note(str(e))
        except Exception as e:
            _note(f"orchestrator.{name}: {type(e).__name__}: {e}")
    # a flag no reader owns (e.g. a retired one) still gets the same type check
    for name in sorted(orch_cfg):
        section = orch_cfg[name]
        if name not in readers and isinstance(section, dict) and "enabled" in section:
            try:
                orch._strict_orchestrator_flag(name, cfg=cfg)
            except ValueError as e:
                _note(str(e))
    halt_policy = orch_cfg.get("halt_policy")
    if isinstance(halt_policy, dict) and "quarantine_enabled" in halt_policy \
            and not isinstance(halt_policy["quarantine_enabled"], bool):
        _note(f"orchestrator.halt_policy.quarantine_enabled={halt_policy['quarantine_enabled']!r} "
              f"is not a real boolean -- write an unquoted `true` or `false` in "
              f"config/campaign_config.yaml")
    if not problems and values.get("variant_anti_adjacency_gate"):
        if not values.get("config_direct_authoring") and not values.get("variant_selection_record"):
            _note("orchestrator.variant_anti_adjacency_gate.enabled=true requires "
                  "orchestrator.variant_selection_record.enabled=true on the legacy "
                  "(config_direct_authoring off) path -- the gate reads "
                  "artifacts/variant_selection.yaml, which only that flag writes")
        elif not (orch.ROOT / orch._CAMPAIGN_MEMORY_REL).exists() and \
                not values.get("regroup_record"):
            _note(f"orchestrator.variant_anti_adjacency_gate.enabled=true requires "
                  f"orchestrator.regroup_record.enabled=true while "
                  f"{orch._CAMPAIGN_MEMORY_REL} does not exist -- nothing would write "
                  f"the memory the gate reads, so every variant would silently ADMIT")
    return values, ("; ".join(problems) or None)


def _flag_preflight_refusal() -> str | None:
    """The refusal half of _flag_preflight (None: the flag set may launch)."""
    return _flag_preflight()[1]


def _promotion_retired_from(values: dict, refusal: str | None) -> bool:
    """C5.6 (D-043): orch._promotion_retired_enabled's value, derived from the
    pre-flight's ONE parsed reading (_flag_preflight) instead of re-reading
    config/campaign_config.yaml: config_direct_authoring AND
    verdict_routing_retired. False on a refused flag set (nothing launches
    then anyway)."""
    return (refusal is None and values.get("config_direct_authoring") is True
            and values.get("verdict_routing_retired") is True)


_PREFLIGHT_TERMINAL_PREFIXES = ("completed", "rejected", "human_pause", "failed_validation")
# The fields a generated protocol is built from (_ensure_protocol_from_constraints).
# O-12: exchange/market_type/venue/drop_feeds exist only for a non-default
# brief venue (absent on both sides otherwise: the comparison is unchanged).
_GENERATED_PROTOCOL_FIELDS = ("symbols", "timeframe", "windows", "holdout", "promotion",
                              "exchange", "market_type", "venue", "drop_feeds")


def _data_spend_evidence(run_dir: Path, run_id: str, state: dict) -> list:
    """Why data may already have been spent on this run (empty: none found): a
    trial row, a protocol_result file (the run's or a variant's), or
    protocol_execution ever entered (completed, attempted, current, audited)."""
    evidence = []
    trials = orch.load_campaign_state().get("trial_sharpes") or []
    if _run_has_trial_row(run_id) or any(
            str(t.get("trial_id", "")).startswith(f"{run_id}:") for t in trials
            if isinstance(t, dict)):
        evidence.append("a trial row in campaign_state.trial_sharpes")
    arts = run_dir / "artifacts"
    results = sorted({p.relative_to(run_dir).as_posix()
                      for p in list(arts.glob("protocol_result*"))
                      + list(arts.glob("variants/*/protocol_result*"))})
    if results:
        evidence.append(f"{results[0]}" + (f" (+{len(results) - 1} more)" if len(results) > 1 else ""))
    if ("protocol_execution" in (state.get("completed_stages") or [])
            or (state.get("stage_attempts") or {}).get("protocol_execution")
            or state.get("current_stage") == "protocol_execution"
            or any(str(k).startswith("protocol_execution") for k in state.get("audit_log") or {})):
        evidence.append("protocol_execution was entered")
    return evidence


def _expected_generated_protocol(generated: dict, run_id: str, *,
                                 promotion_retired: bool, run_dir: Path | None = None) -> dict:
    """The protocol _ensure_protocol_from_constraints would write from these
    machine_constraints.protocol, field for field: same order, same helpers,
    and it raises exactly where generation raises (fourth-round review fix 5 --
    pinned by a parity test over malformed inputs): a missing symbols / start /
    end key, windows reaching the holdout, a `holdout` override disagreeing
    with the policy (CUL-339), no promotion block (unless `promotion_retired`
    -- the pre-flight's reading of config_direct_authoring AND
    verdict_routing_retired -- when the key is always absent, C5.6).
    An empty symbols list is accepted, as generation accepts it.
    O-12: `run_dir` given -> the brief's venue keys and venue symbol names
    through the same helper generation uses (None: no brief, no venue keys)."""
    symbols = generated["symbols"]
    per_symbol_start = generated.get("per_symbol_start") or {}
    start = min(per_symbol_start.values()) if per_symbol_start else generated["start"]
    windows = orch._generate_monthly_windows(start, generated["end"])
    venue_keys: dict = {}
    if run_dir is not None:
        symbols, venue_keys = orch._generated_protocol_venue_keys(run_dir, symbols)
    return {
        "symbols": symbols,
        **venue_keys,
        "timeframe": generated.get("timeframe", "1h"),
        "windows": windows,
        "holdout": orch._generated_protocol_holdout_block(generated),
        **orch._generated_protocol_promotion(generated, run_id,
                                              promotion_retired=promotion_retired),
    }


def _generated_field(doc: dict, key: str):
    """A generated-protocol field for the regeneration diff. C5.6 review fix 9:
    `promotion` absent, null and empty ({}) are the same "no block", so a file
    written with one and expected with another is not regenerated. Under G7
    the expected block is never empty, so the flag-off comparison is
    unchanged."""
    value = doc.get(key)
    return (value or None) if key == "promotion" else value


def _generated_protocol_plan(run_dir: Path, run_id: str, generated: dict, state: dict, *,
                             promotion_retired: bool) -> tuple:
    """(refusal, regeneration) for a machine_constraints.protocol run.

    Spend evidence is checked FIRST (fourth-round review fix 1). Once data may
    have been spent on the run, or protocol_execution completed, the expected
    protocol is never rebuilt from pre_registration.yaml and nothing is ever
    regenerated -- the rules stay those the data was judged by:
      * protocol_execution completed: nothing is checked (as before E-061's
        generated-protocol rules: the protocol was judged at its first use);
      * otherwise the EXISTING generated file gets the D-3 check, nothing more
        (a missing file is refused: run_loop would generate it now, from rules
        that may have changed since the data was seen).
    Before any spend (third-round review fixes 1-2):
      * inputs that would make generation raise are refused up front;
      * no file yet: judged on the pre-registered promotion block (a generated
        file never carries promotion_provenance);
      * a file that matches: judged as it is (a hand ratification holds);
      * a file that differs: refused when anything but `promotion` differs
        (windows, symbols, timeframe, holdout are never rewritten); a
        promotion-only difference returns the regeneration (applied atomically
        before run_loop).
    C5.6: `promotion_retired` comes from the pre-flight's single parsed flag
    reading (no config read here, so a config error is never reported as a
    pre_registration generation error). Under it the expected protocol has no
    `promotion` key; an absent, null or empty block compares equal (no
    spurious regeneration)."""
    path = orch.ROOT / "protocols" / f"{run_id}_generated.json"
    where = f"machine_constraints.protocol (generated {path.name})"
    if "protocol_execution" in (state.get("completed_stages") or []):
        return None, None
    spent = _data_spend_evidence(run_dir, run_id, state)
    if spent:
        if not path.exists():
            return (f"{where}: the generated protocol file is missing although data may already "
                    f"have been spent ({'; '.join(spent)}) -- refusing to let run_loop generate "
                    f"it now from pre_registration.yaml (the rules may have changed since the "
                    f"data was seen). Restore {path.name}"), None
        try:
            protocol_resolution.assert_promotion_ratified(path)
        except protocol_resolution.UngatedProtocolError as e:
            return f"{where}: {e}", None
        return None, None
    try:
        expected = _expected_generated_protocol(generated, run_id,
                                                promotion_retired=promotion_retired,
                                                run_dir=run_dir)
    except Exception as e:
        return (f"{where}: pre_registration.yaml's machine_constraints.protocol cannot generate "
                f"a protocol ({type(e).__name__}: {e}) -- fix it before this run spends "
                f"anything"), None
    generic = (f"[G7/D-3] {where}: the brief's pre-registered promotion block is the abolished "
               f"generic block with no promotion_provenance.ratified_by (a generated protocol "
               f"never carries one), so the protocol would be refused at its first use, after "
               f"1a/1b/2. Pre-register real thresholds for this hypothesis in "
               f"pre_registration.yaml's machine_constraints.protocol.promotion")
    # C5.6: under promotion_retired `expected` carries no `promotion` key; otherwise
    # it always does (G7), so .get() is identical to the old subscript there.
    if not path.exists():
        return (generic if protocol_resolution.promotion_is_generic(expected.get("promotion"))
                else None), None
    try:
        current = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return f"{where}: {path.name} cannot be read ({type(e).__name__}: {e})", None
    differing = [k for k in _GENERATED_PROTOCOL_FIELDS
                 if not isinstance(current, dict)
                 or _generated_field(current, k) != _generated_field(expected, k)]
    if not differing:
        try:
            protocol_resolution.assert_promotion_ratified(path)
        except protocol_resolution.UngatedProtocolError as e:
            return f"{where}: {e}", None
        return None, None
    if differing != ["promotion"]:
        return (f"{where}: {path.name} differs from pre_registration.yaml's "
                f"machine_constraints.protocol in {differing} -- only a promotion-block change "
                f"is regenerated; refusing to rewrite windows, symbols, timeframe or holdout. "
                f"Restore pre_registration.yaml to match {path.name}, or register a new brief"), None
    if protocol_resolution.promotion_is_generic(expected.get("promotion")):
        return generic, None
    return None, {"path": path, "doc": expected, "differing": differing}


def _protocol_preflight(run_dir: Path, run_id: str, *, promotion_retired: bool,
                        ignore_pending: bool = False) -> tuple:
    """(refusal, regeneration): why the protocol this run WILL execute would be
    refused by the D-3 guard (tools/protocol_resolution.assert_promotion_ratified)
    at its first use -- _resolve_protocol_path at 5a / the data gate, after 1a,
    1b and 2 have spent (A3 §3.3, A6) -- or None. Checked before run_loop, so
    before any LLM call; skipped for a terminal pending_stage unless
    `ignore_pending` (the data_block_hitl resume restarts a paused run). Read
    only; a regeneration it returns is applied by _regenerate_protocol.
    `promotion_retired`: _promotion_retired_from(the caller's _flag_preflight).

      * machine_constraints.protocol_ref (a pin), while the backtest is ahead:
        the pinned file, exactly as _ensure_protocol_ref_pinned resolves it. A
        missing file is the pin's own error (run_loop -> stage_exception).
      * machine_constraints.protocol (generated): _generated_protocol_plan --
        also after the backtest (a changed pre-registration is then refused).
      * otherwise, while the backtest is ahead, when the run has a
        run_context.yaml or is the claimed consumer of
        campaign_state.last_escalation: the protocol
        tools/protocol_resolution.resolve_protocol_path selects (the same
        resolver as _resolve_protocol_path), with no state write. Its B10
        refusal is left to run_loop, unchanged."""
    state_path = run_dir / "pipeline_state.yaml"
    state = (orch.load_yaml(state_path) or {}) if state_path.exists() else {}
    if not ignore_pending and \
            (state.get("pending_stage") or "").startswith(_PREFLIGHT_TERMINAL_PREFIXES):
        return None, None
    constraints = orch._load_machine_constraints(run_dir)
    constraints = constraints if isinstance(constraints, dict) else {}
    ref, generated = constraints.get("protocol_ref"), constraints.get("protocol")
    if isinstance(generated, dict) and not ref:
        return _generated_protocol_plan(run_dir, run_id, generated, state,
                                        promotion_retired=promotion_retired)
    if "protocol_execution" in (state.get("completed_stages") or []):
        return None, None
    if isinstance(ref, str) and ref.strip():
        path = orch.ROOT / "protocols" / orch._path_basename_any_os(ref)
        try:
            protocol_resolution.assert_promotion_ratified(path)
        except protocol_resolution.UngatedProtocolError as e:
            return f"machine_constraints.protocol_ref={ref!r}: {e}", None
        return None, None
    run_ctx = run_dir / "artifacts" / "run_context.yaml"
    campaign = orch.load_campaign_state()
    last = campaign.get("last_escalation") or {}
    claimed = bool(last.get("protocol_path")) and last.get("claimed_by_run") == run_id
    if not (run_ctx.exists() or claimed):
        return None, None
    try:
        protocol_resolution.resolve_protocol_path(
            run_dir=run_dir, run_id=run_id, protocols_root=orch.ROOT / "protocols",
            campaign_state=campaign, on_stale_escalation=None)
    except protocol_resolution.UngatedProtocolError as e:
        source = "run_context.yaml" if run_ctx.exists() else \
            f"campaign_state.last_escalation (claimed by {run_id})"
        return f"the protocol resolved from {source}: {e}", None
    except RuntimeError:
        return None, None  # B10 / malformed pin: _resolve_protocol_path raises it, as before
    return None, None


def _protocol_preflight_refusal(run_dir: Path, run_id: str, *, promotion_retired: bool,
                                ignore_pending: bool = False) -> str | None:
    """The refusal half of _protocol_preflight."""
    return _protocol_preflight(run_dir, run_id, promotion_retired=promotion_retired,
                               ignore_pending=ignore_pending)[0]


def _regenerate_protocol(run_id: str, regeneration: dict) -> None:
    """Rewrite a generated protocol whose promotion block changed in
    pre_registration.yaml (pre-spend only; _generated_protocol_plan decided).
    Atomic: a temp file in the same directory, then os.replace -- the original
    is never unlinked first, so a failure leaves it intact."""
    path = regeneration["path"]
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(regeneration["doc"], f, indent=2)
        os.replace(tmp_name, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp_name)
        raise
    _log(f"PROTOCOL {run_id}: {path.name} regenerated before any spend -- field(s) "
         f"{regeneration['differing']} changed in pre_registration.yaml's "
         f"machine_constraints.protocol since it was written.")


def _halt_run(queue: dict, entry: dict, run_id, run_dir, reason: str, detail: str,
              schedulability_enabled: bool) -> bool:
    """A classified pause that also marks the run: status paused_for_human,
    last_error, flags.<reason> (cleared again by a successful --resume). If the
    run's pipeline_state.yaml cannot be written (it may be the cause), the
    queue entry still pauses and the HALT line says so -- no halt_history then."""
    record_run = run_id
    if run_id is not None:
        try:
            orch.update_state(path=run_dir, status="paused_for_human", last_error=detail,
                              flags={reason: True})
        except Exception as state_exc:
            record_run = None
            detail = (f"{detail} [{run_id}: pipeline_state.yaml could not be updated "
                      f"({type(state_exc).__name__}: {state_exc}); no halt_history]")
    return _halt_retired_routing(queue, entry, record_run, reason, detail, schedulability_enabled)


ABANDONED_LAUNCH_STATUS = abandoned_launch.ABANDONED_LAUNCH_STATUS


def _mark_abandoned_launch(run_dir: Path, run_id: str, detail: str) -> None:
    """A run dir a failed launch left behind: status abandoned_launch (its
    pipeline_state.yaml created if setup_run did not get that far), so
    reconcile_orphans never reports it as an unexpected orphan."""
    note = ("E-061 C1.4: this run dir was created by a launch that raised before "
            "run_loop; it spent nothing and is not part of any lineage. The queue "
            "entry records it as launch_failed_run_id.")
    state_path = run_dir / "pipeline_state.yaml"
    if state_path.exists() and orch.load_yaml(state_path):
        orch.update_state(path=run_dir, status=ABANDONED_LAUNCH_STATUS, last_error=detail,
                          abandoned_note=note)
    else:
        orch.save_yaml(state_path, {"run_id": run_id, "status": ABANDONED_LAUNCH_STATUS,
                                    "last_error": detail, "abandoned_note": note,
                                    "audit_log": {}})


def _halt_launch_exception(queue: dict, entry: dict, before: dict, created: list,
                           exc: Exception, schedulability_enabled: bool) -> bool:
    """C1.4 (review fixes 6; third-round 5-6): an exception while launching
    (setup_run, _materialize_run / _materialize_refinement_run,
    _write_brief_hypotheses_context, _launch_queued_card). The entry is put
    back as it was before the launch (a refinement parent stays its last run)
    and records the failed launch explicitly -- launch_failed_run_id (null when
    it raised before allocating one) and launch_exception_detail. A run dir the
    launch created is marked abandoned_launch, never added to run_ids."""
    traceback.print_exc()
    detail = f"{type(exc).__name__}: {exc}"
    entry.clear()
    entry.update(copy.deepcopy(before))
    run_id = created[-1] if created else None
    run_dir = ROOT / "runs" / run_id if run_id else None
    recorded = None
    if run_dir is not None and run_dir.exists():
        try:
            _mark_abandoned_launch(run_dir, run_id, detail)
            recorded = run_id
        except Exception as mark_exc:
            detail = (f"{detail} [{run_id} could not be marked {ABANDONED_LAUNCH_STATUS}: "
                      f"{type(mark_exc).__name__}: {mark_exc}]")
    entry["launch_failed_run_id"] = run_id
    entry["launch_exception_detail"] = detail
    entry["launch_prior_status"] = before.get("status")  # restored by --resume
    if run_id is not None:
        detail = f"{detail} (launching {run_id}, now {ABANDONED_LAUNCH_STATUS})"
    return _halt_retired_routing(queue, entry, recorded, LAUNCH_EXCEPTION_HALT, detail,
                                 schedulability_enabled)


def _record_run_loop_children(queue: dict, entry: dict, run_id: str, before_splits: list,
                              decide_next_enabled: bool) -> tuple:
    """What run_loop left for the queue: split siblings (their own entries) and,
    under decide_next, the brief's extra cards. Run after every run_loop call --
    also one that raised (C1.4 review fix 2), so a sibling recorded before the
    exception is never lost. Returns (queue, entry, split_child_ids)."""
    after_splits = _snapshot_hypothesis_splits()

    # Any hypothesis_generation split(s) that happened anywhere during this run_loop
    # call (whether on run_id itself or an internal reframe/escalate continuation
    # within the same call) get their OWN queue entries — checked before the
    # lineage-continuation logic below so a split sibling is never mistaken for one.
    new_split_events = after_splits[len(before_splits):]
    split_child_ids = set()
    for ev in new_split_events:
        for child_id in ev.get("children", []):
            split_child_ids.add(child_id)
            _add_queue_entry_for_split_child(queue, entry, ev.get("parent_run", run_id), child_id)
    if split_child_ids:
        _save_queue(queue)
        _log(f"SPLIT {entry['id']}: {len(split_child_ids)} sibling hypothesis run(s) "
             f"{sorted(split_child_ids)} each given their own queue entry.")
    if decide_next_enabled:
        # E-059 S2b: the flag-on split left its extra cards in
        # queued_hypotheses.yaml; enqueue them (queued, card_ref). register
        # writes the queue file, so the in-memory queue is reloaded after.
        if _enqueue_queued_hypotheses(entry, run_id):
            queue = _load_queue()
            entry = next(e for e in queue["queue"] if e.get("id") == entry["id"])
    return queue, entry, split_child_ids


def _reapply_split_children(queue: dict, entry: dict, run_id: str, before_splits: list) -> None:
    """Fourth-round review fix 3: after the bookkeeping failed and the queue was
    re-read from disk, add each split sibling that is still missing (best
    effort, idempotent -- an existing `<entry>__split_<child>` is left alone),
    each addition logged. The caller's pause saves the queue."""
    try:
        new_events = _snapshot_hypothesis_splits()[len(before_splits):]
    except Exception as e:
        _log(f"SPLIT {entry['id']}: could not re-read hypothesis_splits to re-apply sibling "
             f"entries ({type(e).__name__}: {e}); check campaign_state.yaml by hand.")
        return
    existing = {e.get("id") for e in queue.get("queue") or [] if isinstance(e, dict)}
    for ev in new_events:
        for child_id in ev.get("children", []):
            if f"{entry['id']}__split_{child_id}" in existing:
                continue
            try:
                _add_queue_entry_for_split_child(queue, entry, ev.get("parent_run", run_id),
                                                 child_id)
                existing.add(f"{entry['id']}__split_{child_id}")
                _log(f"SPLIT {entry['id']}: sibling {child_id} re-applied after the failed "
                     f"bookkeeping (its own queue entry).")
            except Exception as e:
                _log(f"SPLIT {entry['id']}: sibling {child_id} could NOT be re-applied "
                     f"({type(e).__name__}: {e}); add its queue entry by hand.")


def _halt_detached_entry(entry_id: str, run_id: str, run_dir: Path, detail: str,
                         schedulability_enabled: bool) -> bool:
    """Fourth-round review fix 3: the paused entry is gone from the re-read queue
    file. The run is still marked (flags.stage_exception), but the queue file is
    left exactly as re-read -- a detached entry is never saved back into it."""
    record = run_id
    try:
        orch.update_state(path=run_dir, status="paused_for_human", last_error=detail,
                          flags={STAGE_EXCEPTION_HALT: True})
        _append_halt_history(run_dir, orch.load_yaml(run_dir / "pipeline_state.yaml") or {},
                             STAGE_EXCEPTION_HALT, detail)
    except Exception as state_exc:
        record = None
        detail += (f" [{run_id}: pipeline_state.yaml could not be updated "
                   f"({type(state_exc).__name__}: {state_exc}); no halt_history]")
    _log(f"HALT — {STAGE_EXCEPTION_HALT}: {detail}. QUEUE ENTRY {entry_id} IS NOT IN "
         f"config/campaign_queue.yaml after re-reading it -- the queue file was left as "
         f"re-read (nothing saved over it). Restore the entry by hand (run "
         f"{record or run_id}). See RUNBOOK.md §3.")
    _write_loop_health()
    if schedulability_enabled:
        _write_schedulability()
    return False


_LAUNCH_ACTIONS = ("refinement_brief", "fresh_launch", "queued_card")


def _launch_run(queue: dict, entry: dict, action: str, decide_next_enabled: bool,
                created: list, *, promotion_retired: bool) -> str:
    """The launch half of a process_once step (the three launch actions, after
    their own pre-checks), moved here unchanged so process_once can classify an
    exception from any of it (C1.4 review fix 6). `created` receives the new run
    id as soon as it is allocated. Returns the run id to run."""
    if action == "refinement_brief":
        brief_path = ROOT / entry["refinement_brief_path"]
        brief = _parse_refinement_brief_yaml(brief_path)
        child_id = _next_new_run_id()
        created.append(child_id)
        setup_run(child_id)
        _materialize_refinement_run(child_id, brief, brief_path)
        entry["run_ids"].append(child_id)
        entry["refinement_brief_consumed_for"] = entry["refinement_brief_path"]
        _save_queue(queue)
        _log(f"REFINEMENT-BRIEF {entry['id']} -> {child_id} (brief={entry['refinement_brief_path']})")
        return child_id
    if action == "fresh_launch":
        brief_path = ROOT / entry["brief_path"]
        brief = _parse_brief_frontmatter(brief_path)
        run_id = _next_new_run_id()
        created.append(run_id)
        setup_run(run_id)
        _materialize_run(run_id, brief, promotion_retired=promotion_retired)
        if decide_next_enabled:
            # E-059 S2b: a brief run (not a reader candidate) gets the context
            # that lets 1a score extra cards or report the brief exhausted.
            _write_brief_hypotheses_context(queue, entry, run_id)
        entry["run_ids"] = [run_id]
        entry["status"] = "in_progress"
        _save_queue(queue)
        _log(f"LAUNCH {entry['id']} -> {run_id} (brief={entry['brief_path']})")
        return run_id
    # queued_card (its card file was checked before any run dir exists)
    brief = _parse_brief_frontmatter(ROOT / entry["brief_path"])
    run_id = _next_new_run_id()
    created.append(run_id)
    setup_run(run_id)
    _materialize_run(run_id, brief, promotion_retired=promotion_retired)
    _launch_queued_card(entry, run_id)
    entry["run_ids"] = [run_id]
    entry["status"] = "in_progress"
    _save_queue(queue)
    _log(f"LAUNCH-CARD {entry['id']} -> {run_id} (card={entry['card_ref']}, "
         f"brief={entry['brief_path']}; step 1a skipped)")
    return run_id


def _run_after_preflight(queue: dict, entry: dict, run_id: str, before_splits: list,
                         decide_next_enabled: bool, schedulability_enabled: bool, *,
                         promotion_retired: bool):
    """The protocol pre-flight, a pre-spend generated-protocol regeneration and
    run_loop. Returns None when run_loop returned normally, else process_once's
    return value after a classified pause: protocol_promotion_unratified, or
    stage_exception for an Exception escaping any of them (C1.4) -- after the
    split / queued-card bookkeeping, which must not be lost (if that raises
    too, the queue is re-read from disk first, so nothing it registered is
    overwritten). KeyboardInterrupt and SystemExit pass through."""
    run_dir = ROOT / "runs" / run_id
    try:
        refusal, regeneration = _protocol_preflight(run_dir, run_id,
                                                    promotion_retired=promotion_retired)
        if refusal is None:
            if regeneration is not None:
                _regenerate_protocol(run_id, regeneration)
            orch.run_loop(run_id)
    except Exception as exc:
        traceback.print_exc()
        detail = f"{type(exc).__name__}: {exc}"
        try:
            queue, entry, _ = _record_run_loop_children(queue, entry, run_id, before_splits,
                                                        decide_next_enabled)
        except Exception as book_exc:
            detail += (f" [the split / queued-card bookkeeping after it also failed: "
                       f"{type(book_exc).__name__}: {book_exc}]")
            # Fourth-round review fix 3: the queue file is the truth (the failed
            # bookkeeping may have registered entries there). Re-read it, re-apply
            # the split-sibling entries idempotently, and never save an entry that
            # is no longer in it.
            queue = _load_queue()
            found = next((e for e in queue.get("queue") or []
                          if isinstance(e, dict) and e.get("id") == entry["id"]), None)
            if found is None:
                return _halt_detached_entry(entry["id"], run_id, run_dir, detail,
                                            schedulability_enabled)
            entry = found
            _reapply_split_children(queue, entry, run_id, before_splits)
        return _halt_run(queue, entry, run_id, run_dir, STAGE_EXCEPTION_HALT, detail,
                         schedulability_enabled)
    if refusal is not None:
        return _halt_run(queue, entry, run_id, run_dir, PROTOCOL_PREFLIGHT_HALT, refusal,
                         schedulability_enabled)
    return None


def process_once() -> bool:
    """Runs exactly one launch/continue/advance step. Returns True if the
    caller should keep looping, False if the campaign is done or halted."""
    reconcile_orphans()  # A3: read-only, logs only newly-unexpected orphans

    # E-061 C1.5: the flag pre-flight, on every step before anything launches:
    # the config parsed once and handed to every real flag reader. A refusal
    # pauses the selected entry below (never raises). The step's own flag values
    # (schedulability, decide_next, verdict routing) come from this one reading
    # (third-round review fix 9) -- each resolved exactly as its reader resolves
    # it, so a passing step is byte-identical to before.
    flag_values, flag_refusal = _flag_preflight()

    # E-031 S2. Written BEFORE the queue-exhausted check below on EVERY step
    # (not only when exhausted) -- closing E-030's own measured blind spot
    # (all four _write_loop_health() call sites sit after a non-None
    # _select_entry() result). Flag-off: no-op, byte-identical to before
    # this feature existed. E-061 review fix 10: still written, fresh, when the
    # refusal is about another flag and schedulability_block itself reads true.
    schedulability_enabled = flag_values.get("schedulability_block") is True
    if schedulability_enabled:
        _write_schedulability()
    # E-059 S2a / slice 6c S2a: decide_next and verdict_routing_retired, resolved
    # once per step, up front, so a misconfiguration (non-bool, or on without its
    # prerequisite flags) stops before anything launches -- now as a flag refusal.
    decide_next_enabled = flag_refusal is None and flag_values.get("decide_next") is True
    routing_retired = flag_refusal is None and flag_values.get("verdict_routing_retired") is True
    promotion_retired = _promotion_retired_from(flag_values, flag_refusal)  # C5.6

    queue = _load_queue()
    entry = _select_entry(queue["queue"])
    if entry is None:
        if flag_refusal is not None:
            _log(f"HALT — {FLAG_PREFLIGHT_HALT}: {flag_refusal}. No ready or in_progress entry "
                 f"to pause; fix config/campaign_config.yaml before launching. See RUNBOOK.md §3.")
            return False
        _log("Queue exhausted — no ready or in_progress entries remain." + _parked_note(queue))
        return False
    if flag_refusal is not None:
        # Before setup_run: a fresh entry gets no run (--resume re-checks the
        # config and sets it back to ready); an in-progress run gets a
        # halt_history record and keeps its own status.
        return _halt_retired_routing(queue, entry, (entry.get("run_ids") or [None])[-1],
                                     FLAG_PREFLIGHT_HALT, flag_refusal, schedulability_enabled)

    action = _next_action_for_entry(entry)

    if action == "refinement_brief" and routing_retired:
        # Slice 6c S2a (code review item 3): the operator-authored continuation is
        # retired with the routing; never scaffold a child. Register the brief as
        # its own queue entry instead (register_hypothesis / `register`).
        parent = (entry.get("run_ids") or [None])[-1]
        return _halt_retired_routing(
            queue, entry, parent, REFINEMENT_BRIEF_HALT,
            f"refinement_brief_path={entry['refinement_brief_path']!r} would scaffold a "
            f"continuation child under orchestrator.verdict_routing_retired.enabled; no child "
            f"is created. Register the brief as a new entry (run_campaign.py register) and "
            f"remove refinement_brief_path from {entry['id']}", schedulability_enabled)
    if action == "refinement_brief":
        # B1: an operator-authored refinement_brief_path takes precedence
        # over the internal LLM routing's own proposed_brief.yaml — but
        # ONLY if internal routing hasn't already fired for this lineage
        # step. R2: the conflict check runs BEFORE setup_run — a conflicted
        # entry never scaffolds a second child.
        parent_run_id = entry["run_ids"][-1]
        existing_child = _existing_continuation_child(parent_run_id)
        if existing_child:
            reason = "refinement_brief_conflicts_with_existing_continuation"
            detail = (
                f"refinement_brief_path={entry['refinement_brief_path']!r} conflicts with "
                f"existing continuation_child={existing_child!r} already recorded on "
                f"{parent_run_id}'s pipeline_state.yaml (internal routing already fired for "
                f"this lineage step). Resolve by hand per RUNBOOK.md's custody norm (rename "
                f"the internally-scaffolded child per convention, or discard the operator "
                f"override) before resuming."
            )
            entry["status"] = f"paused:{reason}"
            _save_queue(queue)
            _regenerate_summary(queue)
            parent_run_dir = ROOT / "runs" / parent_run_id
            parent_state = orch.load_yaml(parent_run_dir / "pipeline_state.yaml") or {}
            _append_halt_history(parent_run_dir, parent_state, reason, detail)
            _log(f"HALT — {reason}: {detail}. Campaign stopped on {entry['id']} / {parent_run_id}. "
                 f"See RUNBOOK.md 'Resume after a pause'.")
            # E-030 S3. Same BRANCHES as _regenerate_summary, but placed at the END
            # of each one rather than beside it: this instrument reads campaign_log.md
            # and halt_history, both of which are written by the two lines above. Run
            # it where _regenerate_summary sits and every emitted block would be
            # exactly one halt stale, forever.
            _write_loop_health()
            if schedulability_enabled:  # E-031 S2 — same end-of-branch placement
                _write_schedulability()
            return False
    elif action == "queued_card":
        # E-059 S2b (decision 9): the brief's extra card, already authored by 1a
        # in an earlier run -- launched past 1a with that card, as the legacy
        # split sibling was (no second 1a call, no card drift).
        if not (ROOT / str(entry.get("card_ref"))).is_file():
            # Code-review fix 7: checked BEFORE any run dir exists -- pause the
            # entry, no orphan run, no crash.
            reason = "queued_card_missing"
            detail = (f"card_ref={entry.get('card_ref')!r} does not exist; restore the card file "
                      f"(or mark the entry superseded) and set status back to ready")
            entry["status"] = f"paused:{reason}"
            _save_queue(queue)
            _regenerate_summary(queue)
            _log(f"HALT — {reason}: {detail}. Campaign stopped on {entry['id']} (no run "
                 f"created, so no halt_history; this log line is the record). See RUNBOOK.md §3.")
            _write_loop_health()
            if schedulability_enabled:
                _write_schedulability()
            return False
    if action in _LAUNCH_ACTIONS:
        # E-061 C1.4 review fix 6: any exception while launching is a classified
        # pause (launch_exception); a run dir it created is recorded and paused.
        created, before = [], copy.deepcopy(entry)
        try:
            run_id = _launch_run(queue, entry, action, decide_next_enabled, created,
                                 promotion_retired=promotion_retired)
        except Exception as exc:
            return _halt_launch_exception(queue, entry, before, created, exc,
                                          schedulability_enabled)
    else:
        run_id = entry["run_ids"][-1]
        if routing_retired:
            # Slice 6c S2a (code review item 2): never run a lineage step the
            # retired routing minted -- checked BEFORE run_loop spends anything.
            blocker = _legacy_continuation_blocker(entry)
            if blocker:
                return _halt_retired_routing(
                    queue, entry, run_id, LEGACY_CONTINUATION_HALT,
                    f"{blocker}, under orchestrator.verdict_routing_retired.enabled -- decide_next "
                    f"never follows a legacy continuation; a person decides",
                    schedulability_enabled)
            # Slice 6c S2c review fix 3: the run already parked (a crash between
            # its marker and the queue save, or a decide-next failure after the
            # park): finish the park -- never call run_loop on a parked run.
            pre = _run_state(run_id)
            if pre.get("status") == "paused_for_human" and pre.get(orch.PARKED_KEY):
                _log_transition(entry, run_id, pre)
                return _park_entry(queue, entry, run_id, ROOT / "runs" / run_id, pre,
                                   schedulability_enabled)

    run_dir = ROOT / "runs" / run_id
    before_splits = _snapshot_hypothesis_splits()
    # E-061 C1.5 / C1.4: the protocol pre-flight (before 1a), then run_loop; a
    # refusal or an escaping Exception is a classified pause (None: ran normally).
    halted = _run_after_preflight(queue, entry, run_id, before_splits, decide_next_enabled,
                                  schedulability_enabled, promotion_retired=promotion_retired)
    if halted is not None:
        return halted
    queue, entry, split_child_ids = _record_run_loop_children(
        queue, entry, run_id, before_splits, decide_next_enabled)

    state = orch.load_yaml(run_dir / "pipeline_state.yaml")
    _log_transition(entry, run_id, state)

    if routing_retired and state.get("status") == "paused_for_human" and state.get(orch.PARKED_KEY):
        # Slice 6c S2c (S1_FINDINGS_6C.md §6, guess 9): a run waiting on a missing
        # component or missing data parks instead of pausing the campaign. Before
        # _hard_pause_reason, so the E-030 quarantine never sees a parkable reason.
        return _park_entry(queue, entry, run_id, run_dir, state, schedulability_enabled)

    pause = _hard_pause_reason(run_dir, state)
    if pause and pause[0] in _COMPOSITION_FAULT_REASONS and _is_composition_run(entry, run_dir):
        # E-060 S3b (guess 10): a composition run that crashes pauses for the
        # operator -- never quarantined (which would mark it done), never
        # re-fired: R1 fires once per registry state (its queue entry exists).
        # Only entries R1 registered carry this origin (composition_runs on).
        pause = (COMPOSITION_FAILED_REASON, f"{pause[0]}: {pause[1]}")
    if pause:
        reason, detail = pause
        # E-030 S2a. Quarantine + escalate. Everything below the `if` is reached
        # ONLY when the flag is on AND the reason is one of the four the S1 taxonomy
        # classified quarantine-safe on evidence AND the flags dict unambiguously
        # supports that reason. With the flag off, _quarantine_enabled() short-
        # circuits before any of it runs -- no extra log line, no extra state write,
        # no reordering of the escalate path below (EPIC.md Done-when #3).
        if reason in _QUARANTINE_SAFE_REASONS and _quarantine_enabled():
            ambiguity = _flag_ambiguity(state, reason)
            repeat = _repeat_quarantine(state, reason)
            if ambiguity:
                # R11: escalate as today, but say out loud that the check fired.
                # Silent fallback would make an ambiguous halt indistinguishable
                # from an unclassified one -- the exact indistinguishability that
                # let halt #8 be misreported for 0.91h in the first place.
                _log(f"AMBIGUITY — quarantine declined for '{reason}' on "
                     f"{entry['id']} / {run_id}: {ambiguity}. Escalating to a human.")
            elif repeat is not None:
                # E-030 S3 / taxonomy R4, extended from retry to quarantine (the
                # auto-action that actually exists -- see _repeat_quarantine). This
                # is THE decision the loop-health instrument exists to feed: the
                # loop, not a human, reads its own halt record and declines to take
                # the same automatic action twice in a row on the same run.
                #
                # ORDER MATTERS: strictly AFTER R11's ambiguity check. An ambiguous
                # halt already escalates for a prior and different reason, and if
                # this check ran first, a NON-repeating ambiguous halt would take
                # this branch's "clean" path and lose R11's explanation. Nor may
                # this branch override R11 -- an ambiguous halt is never quarantined
                # regardless of what the repeat check says.
                _log(f"REPEAT-ESCALATE — quarantine declined for '{reason}' on "
                     f"{entry['id']} / {run_id}: the immediately preceding halt on "
                     f"this run ({repeat.get('timestamp')}) carried the SAME reason "
                     f"and was auto-quarantined. Taxonomy R4 (same reason code twice "
                     f"in a row on the same run => stop auto-actioning, escalate); "
                     f"the evidenced pair is halts #13/#14, both "
                     f"component_execution_error on run_059. Escalating to a human.")
            else:
                requeueable = reason in _REQUEUEABLE_QUARANTINE_REASONS
                if requeueable:
                    component = _blocked_component_name(run_dir, detail)
                    entry["status"] = f"blocked_on_component:{component}"
                    # No `outcome`: the lineage has not concluded, it is parked
                    # pending engine work (R9 -- "not `done`"). Writing a terminal
                    # outcome onto a re-queueable entry would misreport it as
                    # finished in campaign_summary.md's own table.
                else:
                    # The DONE-path convention, verbatim: `status` says where the
                    # entry stands in the queue, `outcome` says what it concluded.
                    # `done` is what makes the queue ADVANCE past it (_select_entry
                    # never auto-selects `done`), and `outcome` carries the R8 value
                    # instead of a scientific one.
                    entry["status"] = "done"
                    entry["outcome"] = _QUARANTINE_OUTCOME
                    component = None
                decide_msg, keep_going = None, True
                if decide_next_enabled and not requeueable:
                    # E-059 S2a: this path also marks a lineage done, so decide-next
                    # runs here too -- and the entry is persisted `done` only after
                    # the decision (and any minted entry) is on disk (retryable).
                    queue, entry, keep_going, decide_msg = _finish_lineage_with_decision(
                        queue, entry, run_id)
                else:
                    _save_queue(queue)
                _regenerate_summary(queue)
                disposition = _apply_trial_accounting(reason, run_id, detail)
                quarantine_record = {
                    "policy": "E-030 S2a quarantine",
                    "queue_entry_id": entry["id"],
                    "run_id": run_id,
                    "queue_status": entry["status"],
                    "outcome": entry.get("outcome") if not requeueable else None,
                    "requeueable": requeueable,
                    "blocked_on_component": component,
                    "trial_accounting": disposition,
                    # R7's fourth bullet: record the absence as a DECISION. Measured
                    # against campaign_state.trial_sharpes rather than inferred from
                    # the reason -- see the finding noted at _apply_trial_accounting.
                    "no_data_touched": not _run_has_trial_row(run_id),
                    "retry_attempts": [],  # S2a builds no retry; see the section header
                }
                _append_halt_history(run_dir, state, reason, detail,
                                     quarantine=quarantine_record)
                detail_str = f": {detail}" if detail else ""
                _log(f"QUARANTINE — {reason}{detail_str}. {entry['id']} / {run_id} -> "
                     f"status={entry['status']} outcome={entry.get('outcome') or '-'} "
                     f"(trial accounting: {disposition}). Campaign continues; see this "
                     f"run's pipeline_state.yaml halt_history for the full record.")
                if decide_msg:
                    _log(decide_msg)
                _write_loop_health()  # E-030 S3 — see the note at the first call site
                if schedulability_enabled:  # E-031 S2 — same end-of-branch placement
                    _write_schedulability()
                return keep_going
        entry["status"] = f"paused:{reason}"
        _save_queue(queue)
        _regenerate_summary(queue)
        # Read state["last_error"] directly, not the truncated `detail` above --
        # _hard_pause_reason slices last_error to 300 chars for the log line;
        # this append must not inherit that truncation.
        _append_halt_history(run_dir, state, reason, detail)
        detail_str = f": {detail}" if detail else ""
        _log(f"HALT — {reason}{detail_str}. Campaign stopped on {entry['id']} / {run_id}. "
             f"See RUNBOOK.md 'Resume after a pause'.")
        _write_loop_health()  # E-030 S3 — see the note at the first call site
        if schedulability_enabled:  # E-031 S2 — same end-of-branch placement
            _write_schedulability()
        return False

    # A1 (K4 kernel): read the run's own PERSISTED continuation intent
    # (continuation_child, written by _route_refine/_route_pivot/
    # _route_escalate onto their own run's pipeline_state.yaml) instead of
    # diffing runs/ across this call — a continuation across SEPARATE
    # process_once() invocations (fresh process, or this same run reaching
    # its terminal pending_stage in an earlier invocation) now still resolves
    # correctly, since the intent lives on disk, not in this call's locals.
    pending = state.get("pending_stage") or ""
    continuation_child = state.get("continuation_child")
    if routing_retired:
        # Slice 6c S2a (S1_FINDINGS_6C.md guess 12): no route writes
        # continuation_child under the flag, so a continuation here was made by
        # the legacy routing before the flag was switched on. Never followed.
        blocker = _legacy_continuation_blocker(entry)
        if blocker:
            return _halt_retired_routing(
                queue, entry, run_id, LEGACY_CONTINUATION_HALT,
                f"{blocker}, under orchestrator.verdict_routing_retired.enabled -- decide_next "
                f"never follows a legacy continuation; a person decides",
                schedulability_enabled)
        # Code review item 5: fail closed at DONE -- a completed_<idea_status>
        # run must cite a readable, matching idea_status.yaml (never `ungated`).
        if pending in orch.RETIRED_ROUTING_TERMINALS:
            blocker = _idea_status_blocker(run_id, pending)
            if blocker:
                return _halt_retired_routing(queue, entry, run_id, IDEA_STATUS_HALT, blocker,
                                             schedulability_enabled)
    if state.get(orch.CAMPAIGN_REVIEW_REFRAME_KEY):
        # Slice 6c S2b (guess 6): a campaign-review reframe's brief becomes a
        # `ready` queue entry BEFORE decide-next, which alone picks the next run.
        # Only a run whose review the flag's trigger started carries the key.
        # Review fixes 3 + 5: anything that stops the registration -- the flag
        # switched off since, a missing brief, an id collision, a refused
        # registration -- is a classified halt with a halt_history record.
        registered = False
        blocker = _reframe_registration_blocker(run_id, state, routing_retired)
        if blocker is None:
            try:
                registered = _register_campaign_review_reframe(entry, run_id, state)
            except Exception as e:  # classified below, never a raw crash
                blocker = f"registering {state[orch.CAMPAIGN_REVIEW_REFRAME_KEY]} failed: {e}"
        if blocker:
            return _halt_retired_routing(queue, entry, run_id, REFRAME_HALT, blocker,
                                         schedulability_enabled)
        if registered:  # register wrote the queue file: reload it
            queue = _load_queue()
            entry = next(e for e in queue["queue"] if e.get("id") == entry["id"])
    if pending in _LINEAGE_CONTINUATION_STAGES and continuation_child and \
            continuation_child not in split_child_ids:
        entry["run_ids"].append(continuation_child)
        _save_queue(queue)
        _log(f"CONTINUE {entry['id']} lineage {run_id} -> {continuation_child} ({pending})")
        # Review fix 3 (2026-08-26): this was the one non-terminal exit with no
        # end-of-branch write, so the record on disk kept the counts computed at
        # the TOP of the step, before the queue was mutated -- e.g. reporting
        # ready: 1 for an entry this step had already flipped to in_progress,
        # under a computed_at stamped this step. That contradicted the epic's
        # own "a normal step's record is fresh -- not one step stale" claim.
        if schedulability_enabled:
            _write_schedulability()
        return True

    entry["status"] = "done"
    keep_going, decide_msg = True, None
    if decide_next_enabled:
        # E-059 S2a, operator decision 8: the idea's status from the grid, citing
        # idea_status.yaml, instead of `completed_rejected` with no reference
        # (which _save_queue's provenance gate refuses). The entry is persisted
        # `done` only after the decision is on disk (retryable). Flag off: unchanged.
        _apply_idea_status_outcome(entry, run_id, pending or state.get("status"))
        queue, entry, keep_going, decide_msg = _finish_lineage_with_decision(queue, entry, run_id)
    else:
        entry["outcome"] = pending or state.get("status")
        _save_queue(queue)
    _regenerate_summary(queue)
    _log(f"DONE {entry['id']} ({run_id}) -> {entry['outcome']}")
    if decide_msg:
        _log(decide_msg)
    _write_loop_health()  # E-030 S3 — see the note at the first call site
    if schedulability_enabled:  # E-031 S2 — same end-of-branch placement
        _write_schedulability()
    return keep_going


# ---------------------------------------------------------------------------
# E-059 S2a -- decide-next in the DONE branch (delivery_plan_v26.md slice 6b;
# engineering/roadmap/E-059/S1_FINDINGS_6B.md and its operator decision).
# Reached only under orchestrator.decide_next.enabled, only after a lineage is
# marked done. Before slice 6c that means after a refuted idea (or a validated
# one blocked by the deflated-Sharpe gate); every other outcome halts first.
# continuation_child is never read here: under the prerequisite flags no route
# writes it (S1 §1.6), and this branch is reached only after the continuation
# branch above has fallen through.
# ---------------------------------------------------------------------------

_BINDING_IDEA_STATUSES = ("validated", "refuted")
_TRADING_BOT_ROOT = Path(__file__).resolve().parent.parent.parent / "trading-bot"


def _apply_idea_status_outcome(entry: dict, run_id: str, legacy_outcome) -> None:
    """outcome := the grid's idea_status (validated/refuted, citing
    runs/<run>/artifacts/idea_status.yaml, whose result PASS/FAIL is the
    provenance the queue gate accepts; inconclusive needs none). No
    idea_status.yaml (the run ended before the grid, e.g. the data gate's
    decline -> completed_rejected with no backtest): the legacy value, and when
    that value is verdict-bearing it is declared `verdict_status: ungated` --
    true (no grid judged it) and admissible, where a bare completed_rejected
    would make _save_queue refuse the whole queue."""
    ref = f"runs/{run_id}/artifacts/idea_status.yaml"
    doc = orch.load_yaml(ROOT / ref) if (ROOT / ref).exists() else None
    status = doc.get("idea_status") if isinstance(doc, dict) else None
    if status in _BINDING_IDEA_STATUSES:
        entry["outcome"] = status
        entry["pass_rule_evaluation_ref"] = ref
    elif status == "inconclusive":
        entry["outcome"] = status
    else:
        entry["outcome"] = legacy_outcome
        if vce.outcome_is_verdict_bearing(legacy_outcome) and not entry.get("pass_rule_evaluation_ref"):
            entry["verdict_status"] = "ungated"
            entry["verdict_status_basis"] = (
                f"no idea_status.yaml for {run_id}: the run ended at {legacy_outcome} before "
                f"the grid judged the idea (E-059 S2a DONE branch)")


QUEUE_EXHAUSTED_WITH_OPEN_BRIEFS = "queue_exhausted_with_open_briefs"  # RUNBOOK §3 row


def _parked_note(queue: dict) -> str:
    """Slice 6c S2c (guess 13): appended to the loop's stop lines ("Queue
    exhausted" and a decide-next stop) when parked entries remain, naming them
    and the RUNBOOK row. Empty when none is parked -- always, with the flag off."""
    parked = [e.get("id") for e in (queue.get("queue") or [])
              if isinstance(e, dict) and str(e.get("status", "")).startswith(PARKED_STATUS_PREFIX)]
    if not parked:
        return ""
    return (f" Parked, waiting for a component or data: {parked} -- unpark with --unpark <id> "
            f"(RUNBOOK.md §3 {QUEUE_EXHAUSTED_WITH_OPEN_BRIEFS}).")


def _park_entry(queue: dict, entry: dict, run_id: str, run_dir: Path, state: dict,
                schedulability_enabled: bool) -> bool:
    """Slice 6c S2c. The run carries a parked marker (run_phase1_research._park_run):
    the entry becomes paused:waiting_for_<kind> with parked_reason, a halt_history
    record carries the marker, a PARKED line is logged, and decide-next picks the
    next run. The decision record gets its own name, so the run's later DONE
    decision never overwrites it. Returns keep_going.

    Retryable, like the DONE branch (review fix 4): the entry is persisted parked
    only by _finish_lineage_with_decision, AFTER the decision is on disk. If
    deciding fails, the entry is left as it was (in_progress) and the next
    process_once re-enters here BEFORE run_loop (review fix 3), so the parked
    run is never re-run and the decision is retried. The halt_history record
    and the PARKED line are written once per park (keyed on the marker's
    parked_at), never again on a retry."""
    marker = state[orch.PARKED_KEY]
    kind = marker.get("kind") if isinstance(marker, dict) else None
    if kind not in orch.PARK_KINDS:
        raise RuntimeError(f"{run_id}: pipeline_state.yaml {orch.PARKED_KEY}={marker!r} has no "
                           f"known kind {orch.PARK_KINDS}")
    reason = f"waiting_for_{kind}"
    refs = list(marker.get("request_refs") or [])
    detail = f"{kind} at {marker.get('stage')}: {marker.get('reason')}"
    history = [h for h in state.get("halt_history") or [] if isinstance(h, dict)]
    if history and (history[-1].get("parked") or {}).get("parked_at") == marker.get("parked_at"):
        _log(f"PARKED {entry['id']} / {run_id}: retrying the decision after this park ({detail}).")
    else:
        _append_halt_history(run_dir, state, reason, detail, parked=dict(marker))
        history.append({"parked": marker})
        _log(f"PARKED {entry['id']} / {run_id}: {detail}. Requests: {refs}. The campaign "
             f"continues; unpark with --unpark {entry['id']} (RUNBOOK.md §4).")
    entry["status"] = f"{PARKED_STATUS_PREFIX}{kind}"
    entry["parked_reason"] = f"{reason} at {marker.get('stage')}: {marker.get('reason')}"
    # One directory per park (the n-th park of this run), stable across retries;
    # same file name, so save_yaml's schema check applies.
    n = sum(1 for h in history if "parked" in h)
    queue, entry, keep_going, decide_msg = _finish_lineage_with_decision(
        queue, entry, run_id,
        decision_ref=f"runs/{run_id}/artifacts/parked/park_{n}/decision_record.yaml",
        trigger_extra={"parked": kind})
    _regenerate_summary(queue)
    _log(decide_msg)
    _write_loop_health()
    if schedulability_enabled:
        _write_schedulability()
    return keep_going


def _finish_lineage_with_decision(queue: dict, entry: dict, run_id: str, *,
                                  decision_ref: str | None = None,
                                  trigger_extra: dict | None = None) -> tuple:
    """Decide next, then persist the finished entry -- in that order, so a
    failure anywhere leaves the entry NOT done on disk (still in_progress):
    the next process_once selects it again, its run_loop is a no-op on the
    terminal run, and the decision is retried.

    `entry` (inside `queue`) already carries its final status/outcome IN MEMORY
    ONLY. Order: decide on that final queue (tools/decide_next.py, with this
    module's _select_entry as the scheduling rule) -> if a candidate is picked,
    refuse a colliding id/brief, write the brief, register it (rolled back if
    registration fails) -> write decision_record.yaml -> reload the queue from
    disk, put the final entry in, save. No record ever claims a pick that has
    no queue entry. Returns (queue, entry, keep_going, decide_log_line)."""
    import copy as _copy
    import decide_next as dn  # tools/ sibling (on sys.path, see the imports above)
    # E-059 S2b: field changes to OTHER entries (and the finished one), applied
    # to the in-memory queue before deciding and to the disk queue at the end.
    updates = _brief_updates(queue, entry)
    _apply_updates(queue.get("queue") or [], updates)
    final_queue = _copy.deepcopy(queue)
    digest_path = ROOT / "campaign_record" / "exclusion_digest.yaml"
    digest = orch.load_yaml(digest_path) if digest_path.exists() else None
    known = (dn.known_component_classes(_TRADING_BOT_ROOT)
             if (_TRADING_BOT_ROOT / "strategies" / "strategy_components.py").exists() else None)
    # E-035 S2c: the feed set a requires_feed proposal is checked against,
    # read lazily -- load_inputs calls it only when some proposal carries
    # requires_feed, and it then fails loud if the registry is unreadable.
    def feeds():
        return dn.load_feed_set(_TRADING_BOT_ROOT)
    # E-060 S3b: R1's inputs only under orchestrator.composition_runs (the kwargs
    # only when on, so the flag-off call is unchanged).
    comp_on = orch._composition_runs_enabled()

    def _decide():
        inputs = dn.load_inputs(
            ROOT, final_queue, categories=orch._reader_categories(), known_classes=known,
            digest=digest, feed_set=feeds,
            **({"composition_runs": True, "dsr_basis": _ledger_dsr_basis()} if comp_on else {}))
        mem_entry = (inputs["memory"].get("runs") or {}).get(run_id) or {}
        trigger = {"after_run": run_id, "after_entry": entry["id"],
                   "idea_status": mem_entry.get("idea_status")}
        trigger.update(trigger_extra or {})  # slice 6c S2c: {"parked": kind}; else nothing
        return inputs, dn.decide(inputs, now=datetime.now(timezone.utc).isoformat(),
                                 trigger=trigger, select_entry=_select_entry)
    inputs, record = _decide()
    decision_ref = decision_ref or f"runs/{run_id}/artifacts/decision_record.yaml"
    prepared, r1_failures = None, []
    # Review fix 2: a composition that cannot be prepared is paused on its own
    # (failure row -> R1 treats that block set as fired) and the decision is
    # made again; each pass removes one block set, so this ends.
    while comp_on and (record.get("picked") or {}).get("composition"):
        try:
            prepared = _prepare_r1(record, inputs, decision_ref)
            break
        except _CompositionPrepFailed as err:
            # the failure row (read by R1 before anything else) keeps this
            # block set from being picked again
            r1_failures.append(_record_r1_failure(record, err, entry, run_id, decision_ref))
            inputs, record = _decide()
    picked, stop = record.get("picked") or {}, record.get("stop")

    if picked.get("candidate_id") and picked.get("card_ref"):
        # E-059 S2b: the top candidate is a brief's waiting extra card.
        cid = picked["queue_entry_id"]
        updates.setdefault(cid, {}).update({"status": "ready", "decision_ref": decision_ref})
        msg = (f"DECIDE after {entry['id']} ({run_id}): picked extra card {cid} "
               f"(queued -> ready, card={picked['card_ref']}). Record: {decision_ref}")
    elif picked.get("r2_request"):
        msg = _apply_r2(record, final_queue, decision_ref, updates, entry, run_id)
    elif picked.get("composition"):
        msg = _register_r1(record, prepared, decision_ref, entry, run_id)
    elif picked.get("candidate_id"):
        cid = picked["queue_entry_id"]
        rel, text = dn.candidate_brief(record, inputs, decision_ref=decision_ref)
        brief_path = ROOT / rel
        on_disk_ids = {e.get("id") for e in _load_queue().get("queue") or [] if isinstance(e, dict)}
        if cid in on_disk_ids or brief_path.exists():
            raise RuntimeError(f"decide_next: queue id or brief for {cid!r} already exists "
                               f"({brief_path}); refusing before anything is written")
        cand = next(c for c in record["candidates"] if c["candidate_id"] == picked["candidate_id"])
        brief_path.parent.mkdir(parents=True, exist_ok=True)
        brief_path.write_text(text, encoding="utf-8")
        try:
            rc = register_hypothesis(
                brief_path, dn.AGENT_PRIORITY,
                # Scores stay in the decision record only (S1 §8): never in the queue.
                f"decide_next after {run_id}: {cand['kind']} from {cand['proposal_ref']} "
                f"(rank {cand['rank']}; see decision_ref)",
                entry_id=cid, source="agent", relation=None,
                extra={"origin": dn.ORIGIN_READER, "proposal_ref": cand["proposal_ref"],
                       "decision_ref": decision_ref})
            if rc != 0:
                raise RuntimeError(f"decide_next: registering {cid!r} was refused (see the "
                                   f"REGISTER line above)")
        except BaseException:
            brief_path.unlink(missing_ok=True)  # never leave a brief with no queue entry
            raise
        msg = (f"DECIDE after {entry['id']} ({run_id}): picked {picked['candidate_id']} "
               f"-> queue entry {cid} (ready). Record: {decision_ref}")
    elif stop:
        msg = (f"DECIDE stop after {entry['id']} ({run_id}): {stop['reason']} -- "
               f"{stop.get('detail')}. Record: {decision_ref}. See RUNBOOK.md §3."
               + _parked_note(final_queue))
    else:
        nxt = picked.get("operator_entry") or picked.get("queue_entry_id")
        msg = (f"DECIDE after {entry['id']} ({run_id}): the scheduler runs {nxt} next "
               f"({'operator' if picked.get('operator_entry') else 'agent'} entry). "
               f"Record: {decision_ref}")
    if r1_failures:  # E-060 S3b review fix 2 (composition_runs only)
        msg = f"{msg} [paused {len(r1_failures)} composition(s) that could not be prepared]"

    orch.save_yaml(ROOT / decision_ref, record)
    disk_queue = _load_queue()
    items = disk_queue.get("queue") or []
    idx = next((i for i, e in enumerate(items) if isinstance(e, dict) and e.get("id") == entry["id"]),
               None)
    if idx is None:
        raise RuntimeError(f"decide_next: queue entry {entry['id']!r} vanished from disk")
    items[idx] = entry
    _apply_updates(items, updates)
    _save_queue(disk_queue)
    return disk_queue, entry, stop is None, msg


# ---------------------------------------------------------------------------
# E-059 S2b -- briefs (card M), brief status, R2, legacy briefs. Flag-on only:
# every caller sits behind orch._decide_next_enabled().
# ---------------------------------------------------------------------------

def _apply_updates(items: list, updates: dict) -> None:
    for e in items:
        if isinstance(e, dict) and e.get("id") in updates:
            e.update(updates[e["id"]])


def _brief_updates(queue: dict, entry: dict) -> dict:
    """{entry_id: {field: value}} to write with this decision:
      * the brief's owner flips to `brief_status: exhausted` when the finished
        run ended completed_brief_exhausted (step 1a said so; nothing else does);
      * operator decision 7: every legacy brief (no brief_status) not yet
        tagged gets `title: "[obsolete] <brief heading or id>"` -- once (an
        entry already carrying the marker is skipped), on the QUEUE ENTRY
        only; the brief file is read for its heading, never written.
      * R2 MUST TERMINATE (code-review fix 1): an open owner whose last
        decide_next.BRIEF_MAX_CONSECUTIVE_EMPTY_R2 finished R2 requests all
        yielded no new, eligible card (repeat, quarantine, failure/pause,
        superseded) flips to exhausted with brief_status_reason
        `no_new_hypothesis`.
    None of these changes a status the scheduler picks by."""
    import decide_next as dn
    items = [e for e in queue.get("queue") or [] if isinstance(e, dict)]
    updates: dict = {}
    if entry.get("outcome") == dn.BRIEF_EXHAUSTED_OUTCOME:
        owner = dn.brief_owner(entry, items)
        if owner is not None:
            updates.setdefault(owner["id"], {}).update(
                {"brief_status": dn.BRIEF_EXHAUSTED, "brief_status_reason": "step_1a_reported"})
    for e in items:
        if e.get("brief_status") == dn.BRIEF_OPEN and e["id"] not in updates:
            streak = dn.consecutive_empty_r2(e, items)
            if len(streak) >= dn.BRIEF_MAX_CONSECUTIVE_EMPTY_R2:
                updates[e["id"]] = {"brief_status": dn.BRIEF_EXHAUSTED,
                                    "brief_status_reason": dn.AUTO_EXHAUSTED_REASON}
                _log(f"BRIEF-EXHAUSTED {e['id']}: {len(streak)} consecutive R2 requests "
                     f"{streak} yielded no new hypothesis (limit "
                     f"{dn.BRIEF_MAX_CONSECUTIVE_EMPTY_R2}).")
    for e in items:
        if dn.needs_obsolete_tag(e):
            updates.setdefault(e["id"], {})["title"] = dn.obsolete_title(
                e, dn.brief_heading(ROOT, e.get("brief_path")))
    return updates


def _apply_r2(record: dict, final_queue: dict, decision_ref: str, updates: dict,
              entry: dict, run_id: str) -> str:
    """Register R2's new requests (origin brief, on the owner's brief file,
    priority 999, no relation), all `ready`, and flip every reused waiting
    request to ready. Refuses a colliding id before any write."""
    import decide_next as dn
    r2 = record["rules"]["r2"]
    by_id = {e.get("id"): e for e in final_queue.get("queue") or [] if isinstance(e, dict)}
    on_disk = {e.get("id") for e in _load_queue().get("queue") or [] if isinstance(e, dict)}
    clash = [q["entry_id"] for q in r2["enqueued"] if q["entry_id"] in on_disk]
    if clash:
        raise RuntimeError(f"decide_next R2: queue id(s) {clash} already exist; refusing")
    for q in r2["enqueued"]:
        owner = by_id[q["owner"]]
        rc = register_hypothesis(
            ROOT / owner["brief_path"], dn.AGENT_PRIORITY,
            f"R2 after {run_id}: ask step 1a for more hypotheses on open brief {q['owner']} "
            f"(see decision_ref)",
            entry_id=q["entry_id"], source="agent", relation=None,
            extra={"origin": dn.ORIGIN_BRIEF, "decision_ref": decision_ref}, status=q["status"])
        if rc != 0:
            raise RuntimeError(f"decide_next R2: registering {q['entry_id']!r} was refused")
    new_ids = {q["entry_id"] for q in r2["enqueued"]}
    for rid in r2["ready"]:  # code-review fix 3: every waiting request becomes schedulable
        if rid not in new_ids:
            updates.setdefault(rid, {}).update({"status": "ready", "decision_ref": decision_ref})
    return (f"DECIDE after {entry['id']} ({run_id}): R2 -- {len(r2['eligible_briefs'])} eligible "
            f"open brief(s); ready: {r2['ready']} ({len(new_ids)} new); the scheduler runs "
            f"{record['picked']['queue_entry_id']} first. Record: {decision_ref}")


class _CompositionPrepFailed(RuntimeError):
    """R1's preparation of one composition failed (a CompositionError,
    CompositeError or DecideNextError underneath). Classified by
    _record_r1_failure, never a raw traceback (review fix 2)."""


def _ledger_dsr_basis() -> dict:
    """The trial ledger's current deflated-Sharpe basis {n_dsr_total,
    n_trials} (the promotion audit's own counts): R1 re-fires a composition
    that was inconclusive for want of trials only once these allow a DSR
    (review fix 1). Read only."""
    ctx = orch._promotion_dsr_context()
    return {"n_dsr_total": ctx["n_dsr_total"], "n_trials": ctx["n_trials"]}


def _prepare_r1(record: dict, inputs: dict, decision_ref: str) -> dict:
    """E-060 S3b: R1 picked a composition (only under
    orchestrator.composition_runs). Code, not an LLM, writes, in this order,
    each step idempotent so a retried decision redoes it byte for byte:
      1. each block's stand-alone daily returns from its validating run
         (tools/composition.load_daily_returns_by_block -- fails loud when
         missing or short) and, per composite window, its residual IC on the
         data before that window (load_block_prior_residual_ic);
      2. the three variant configs + composition_manifest.yaml under
         campaign_record/compositions/<entry id>/ (write_composition_variants;
         vol_scaled / ic_weighted weights per window, estimated only from data
         before each window -- review fix 5);
      3. the campaign_record/compositions.yaml entry (record_composition).
    Returns {rel, text, blocks, out_dir} for _register_r1. Any
    CompositionError / CompositeError / DecideNextError raises
    _CompositionPrepFailed before any queue entry exists."""
    import decide_next as dn
    import composite_cache as cc
    import composition as comp
    picked = record["picked"]
    eid = picked["composition"]
    registry = inputs["composition"]["registry"]
    try:
        blocks, _excluded = cc.forecast_blocks_on_timeframe(registry, picked["timeframe"])
        if len(blocks) < 2 or cc.composite_registry_hash(blocks) != picked["registry_hash"]:
            raise dn.DecideNextError(f"the registry's blocks on {picked['timeframe']} no longer "
                                     f"hash to {picked['registry_hash']}")
        on_disk = {e.get("id") for e in _load_queue().get("queue") or [] if isinstance(e, dict)}
        if eid in on_disk:
            raise dn.DecideNextError(f"queue id {eid!r} already exists")
        out_dir = ROOT / dn.COMPOSITIONS_DIR / eid
        returns = comp.load_daily_returns_by_block(blocks, root=ROOT)
        starts = dn.composition_window_starts(inputs, [b["block_id"] for b in blocks])
        tf = picked["timeframe"]
        manifest = comp.write_composition_variants(
            registry, tf, out_dir, root=ROOT, daily_returns_by_block=returns,
            window_starts=starts,
            prior_ic=lambda b, d: comp.load_block_prior_residual_ic(b, d, root=ROOT, timeframe=tf),
            enabled=True)
        manifest_ref = (out_dir / comp.MANIFEST_FILENAME).relative_to(ROOT).as_posix()
        rel, text = dn.composition_brief(record, inputs, manifest, manifest_ref=manifest_ref,
                                         manifest_sha256=dn.config_sha256(manifest),
                                         decision_ref=decision_ref)
        comp.record_composition(ROOT / dn.COMPOSITIONS_FILE,
                                comp.composition_entry(manifest, manifest_ref), root=ROOT,
                                enabled=True)
    except (comp.CompositionError, cc.CompositeError, dn.DecideNextError) as e:
        raise _CompositionPrepFailed(f"R1 picked {eid} but it could not be prepared: {e}") from e
    return {"rel": rel, "text": text, "blocks": blocks, "out_dir": out_dir}


def _record_r1_failure(record: dict, err: Exception, entry: dict, run_id: str,
                       decision_ref: str) -> str:
    """Review fix 2: a composition that could not be prepared becomes a
    CLASSIFIED pause of that composition only -- a failure row in
    compositions.yaml (R1 treats the block set as fired: never re-tried by
    code), a queue entry `paused:composition_failed` (origin composition, no
    run), and a halt_history record on the finished run whose decision fired
    it. The decision is then made again without it, so the campaign keeps
    running other candidates. Returns the log line."""
    import decide_next as dn
    import composition as comp
    picked = record["picked"]
    eid = picked["composition"]
    reason = str(err)
    comp.record_composition_failure(ROOT / dn.COMPOSITIONS_FILE,
                                    registry_hash=picked["registry_hash"],
                                    timeframe=picked["timeframe"], entry_id=eid, reason=reason,
                                    enabled=True)
    queue = _load_queue()
    if not any(isinstance(e, dict) and e.get("id") == eid for e in queue.get("queue") or []):
        queue["queue"].append({
            "id": eid, "brief_path": dn.COMPOSITIONS_FILE,
            "status": f"paused:{COMPOSITION_FAILED_REASON}", "priority": picked["priority"],
            "source": "agent",
            "notes": (f"R1 after {run_id}: composition of {picked['timeframe']} blocks "
                      f"(registry_hash {picked['registry_hash']}) could not be prepared -- see "
                      f"{dn.COMPOSITIONS_FILE} failures and RUNBOOK.md §3 "
                      f"{COMPOSITION_FAILED_REASON}"),
            "run_ids": [], "origin": dn.ORIGIN_COMPOSITION, "decision_ref": decision_ref})
        _save_queue(queue)
    run_dir = ROOT / "runs" / run_id
    state = orch.load_yaml(run_dir / "pipeline_state.yaml") or {}
    _append_halt_history(run_dir, state, COMPOSITION_FAILED_REASON, f"{eid}: {reason}")
    msg = (f"HALT — {COMPOSITION_FAILED_REASON}: {eid}: {reason[:300]}. The composition is "
           f"paused (queue {eid} paused:{COMPOSITION_FAILED_REASON}, failure row in "
           f"{dn.COMPOSITIONS_FILE}); the campaign continues. See RUNBOOK.md §3.")
    _log(msg)
    return msg


def _register_r1(record: dict, prepared: dict, decision_ref: str, entry: dict,
                 run_id: str) -> str:
    """Write the brief and register the queue entry (origin composition, R1's
    priority; the brief is removed again if the registration is refused)."""
    import decide_next as dn
    picked = record["picked"]
    eid = picked["composition"]
    brief_path = ROOT / prepared["rel"]
    wrote = False
    if brief_path.exists():
        if brief_path.read_text(encoding="utf-8") != prepared["text"]:
            raise RuntimeError(f"{COMPOSITION_FAILED_REASON}: {brief_path} exists with other "
                               f"content; refusing to overwrite a brief")
    else:
        brief_path.parent.mkdir(parents=True, exist_ok=True)
        brief_path.write_text(prepared["text"], encoding="utf-8")
        wrote = True
    blocks, out_dir = prepared["blocks"], prepared["out_dir"]
    try:
        rc = register_hypothesis(
            brief_path, picked["priority"],
            f"R1 after {run_id}: composition of {len(blocks)} forecast blocks on "
            f"{picked['timeframe']} (code-written variants {out_dir.relative_to(ROOT).as_posix()}; "
            f"see decision_ref)",
            entry_id=eid, source="agent", relation=None,
            extra={"origin": dn.ORIGIN_COMPOSITION, "decision_ref": decision_ref})
        if rc != 0:
            raise RuntimeError(f"decide_next R1: registering {eid!r} was refused")
    except BaseException:
        if wrote:
            brief_path.unlink(missing_ok=True)  # never leave a brief with no queue entry
        raise
    return (f"DECIDE after {entry['id']} ({run_id}): R1 -- composition {eid} of "
            f"{[b['block_id'] for b in blocks]} on {picked['timeframe']} (ready, priority "
            f"{picked['priority']}; variants + manifest written by code). Record: {decision_ref}")


def _write_brief_hypotheses_context(queue: dict, entry: dict, run_id: str) -> None:
    """runs/<run>/artifacts/brief_hypotheses_context.yaml for a run of a brief
    that has an owner (the owner itself, or an origin-brief request). Its presence gives step 1a
    the BRIEF_HYPOTHESES.md addendum; `already_produced` lists the hypothesis
    ids this brief file has produced so far (every entry sharing it)."""
    import decide_next as dn
    items = [e for e in queue.get("queue") or [] if isinstance(e, dict)]
    owner = dn.brief_owner(entry, items)
    if owner is None:
        # Code-review fix 9: a reader candidate or a LEGACY brief (no
        # brief_status, operator decision 7) gets no context, hence no addendum.
        return
    doc = {
        "schema_version": 1,
        "queue_entry": entry["id"],
        "brief_owner": owner["id"] if owner else None,
        "brief_path": entry.get("brief_path"),
        "request": "more_hypotheses" if dn.is_r2_request(entry) else "first_launch",
        "already_produced": dn.brief_hypothesis_ids(ROOT, queue, entry.get("brief_path")),
    }
    orch.save_yaml(ROOT / "runs" / run_id / "artifacts" / orch.BRIEF_CONTEXT_FILE, doc)


def _launch_queued_card(entry: dict, run_id: str) -> None:
    """Copy the saved card into the new run and start it at the stage after
    1a, as run_loop would (strategy_config_authoring under config-direct
    authoring, else innovation_expansion)."""
    src = ROOT / entry["card_ref"]
    if not src.is_file():
        raise FileNotFoundError(f"queued card {src} for entry {entry['id']!r} is missing")
    run_dir = ROOT / "runs" / run_id
    shutil.copy(src, run_dir / "artifacts" / "hypothesis_card.yaml")
    nxt = ("strategy_config_authoring" if orch._config_direct_authoring_enabled()
           else "innovation_expansion")
    orch.update_state(path=run_dir, pending_stage=nxt, current_stage="hypothesis_generation",
                      completed_stages=["hypothesis_generation"], status="active")
    # The run skips 1a, so do what 1a's completion does: write pre_registration's
    # pass_rule from this card's criteria (a criteria_from-1a brief; no-op
    # otherwise) and run the specialist_readers pre-flight. Without it the
    # pass_rule stays null and run_loop's pre-flight refuses the run (found on
    # C4 run_064, the first queued-card launch, 2026-10-02). Raises before spend.
    orch._write_pass_rule_from_card(run_dir, run_id, orch._specialist_readers_enabled())


def _enqueue_queued_hypotheses(entry: dict, run_id: str) -> bool:
    """Register each extra card listed in runs/<run>/artifacts/queued_hypotheses.yaml
    (queued, origin brief, card_ref, priority 999, id <entry>__h<n>), then mark
    the file enqueued. Idempotent: an entry already holding that id and
    card_ref is skipped; the same id with another card raises. Returns True
    when anything was registered."""
    import decide_next as dn
    path = ROOT / "runs" / run_id / "artifacts" / dn.QUEUED_HYPOTHESES_FILE
    if not path.exists():
        return False
    doc = orch.load_yaml(path) or {}
    if doc.get("enqueued"):
        return False
    # Code-review fix 2: only from a run whose step 1a COMPLETED and that has not
    # failed -- never from a run whose 1a output was refused (the split or a
    # later 1a check raised) or that failed.
    state = orch.load_yaml(ROOT / "runs" / run_id / "pipeline_state.yaml") or {}
    if (state.get("status") == "failed"
            or "hypothesis_generation" not in (state.get("completed_stages") or [])):
        _log(f"QUEUED-CARDS {entry['id']} ({run_id}): NOT enqueued -- step 1a did not complete "
             f"cleanly (status={state.get('status')!r}).")
        return False
    existing = {e.get("id"): e for e in _load_queue().get("queue") or [] if isinstance(e, dict)}
    wrote = False
    for card in doc.get("cards") or []:
        cid = f"{entry['id']}__h{card['n']}"
        if cid in existing:
            if existing[cid].get("card_ref") != card["card_ref"]:
                raise RuntimeError(f"queue id {cid!r} exists with another card; refusing")
            continue
        rc = register_hypothesis(
            ROOT / entry["brief_path"], dn.AGENT_PRIORITY,
            f"Extra hypothesis {card['hypothesis_id']} from {run_id}'s step 1a "
            f"(multi-card brief; ranked by its 1a scores, see {path.relative_to(ROOT).as_posix()})",
            entry_id=cid, source="agent", relation=None,
            extra={"origin": dn.ORIGIN_BRIEF, "card_ref": card["card_ref"]}, status="queued")
        if rc != 0:
            raise RuntimeError(f"registering extra card {cid!r} was refused")
        wrote = True
    doc["enqueued"] = True
    orch.save_yaml(path, doc)
    _log(f"QUEUED-CARDS {entry['id']} ({run_id}): {len(doc.get('cards') or [])} extra "
         f"hypothesis card(s) in the queue as `queued`.")
    return wrote


def _reframe_registration_blocker(run_id: str, state: dict, routing_retired: bool) -> str | None:
    """Slice 6c S2b review fixes 3 + 5. Why the run's campaign-review reframe
    brief (pipeline_state.yaml orch.CAMPAIGN_REVIEW_REFRAME_KEY) cannot be
    registered now, or None (also None when there is no brief, or it is
    already registered). Read-only; used at DONE and by --resume."""
    rel = state.get(orch.CAMPAIGN_REVIEW_REFRAME_KEY)
    if not rel:
        return None
    if not routing_retired:
        return (f"{run_id}'s campaign review wrote the reframe brief {rel} under "
                f"orchestrator.verdict_routing_retired.enabled, but the flag is now off -- the "
                f"brief is never dropped silently. Switch the flag back on and --resume (it is "
                f"then registered), or register it by hand and remove "
                f"{orch.CAMPAIGN_REVIEW_REFRAME_KEY} from runs/{run_id}/pipeline_state.yaml")
    if not (ROOT / rel).is_file():
        return (f"{run_id}'s reframe brief {rel} is missing (restore it, or remove "
                f"{orch.CAMPAIGN_REVIEW_REFRAME_KEY} from runs/{run_id}/pipeline_state.yaml)")
    new_id = Path(rel).stem
    prior = next((e for e in _load_queue().get("queue") or []
                  if isinstance(e, dict) and e.get("id") == new_id), None)
    if prior is not None and not (prior.get("brief_path") == rel
                                  and prior.get("origin") == orch.CAMPAIGN_REVIEW_ORIGIN):
        return (f"queue id {new_id!r} already exists with another brief or origin "
                f"(brief={prior.get('brief_path')!r}, origin={prior.get('origin')!r}); rename "
                f"one of them")
    return None


def _register_campaign_review_reframe(entry: dict, run_id: str, state: dict) -> bool:
    """Slice 6c S2b (S1_FINDINGS_6C.md guess 6), under
    orchestrator.verdict_routing_retired only, once
    _reframe_registration_blocker has returned None. Registers the reframe
    brief as a `ready` entry -- id = the brief's stem, priority
    decide_next.AGENT_PRIORITY, source agent, no relation, origin
    campaign_review. Nothing else: no run, no pick (decide-next records the
    pick). An entry already holding that id (the blocker has checked it is
    this brief) is skipped: a retried DONE step. A refused registration
    raises; the caller turns it into a classified halt. Returns True when an
    entry was registered."""
    rel = state.get(orch.CAMPAIGN_REVIEW_REFRAME_KEY)
    if not rel:
        return False
    import decide_next as dn
    brief_path = ROOT / rel
    new_id = brief_path.stem
    if any(isinstance(e, dict) and e.get("id") == new_id for e in _load_queue().get("queue") or []):
        return False
    rc = register_hypothesis(
        brief_path, dn.AGENT_PRIORITY,
        f"Reframe from {run_id}'s campaign review (runs/{run_id}/artifacts/campaign_review.yaml)",
        entry_id=new_id, source="agent", relation=None,
        extra={"origin": orch.CAMPAIGN_REVIEW_ORIGIN}, status="ready")
    if rc != 0:
        raise RuntimeError(f"registering {new_id!r} was refused (see the REGISTER line above)")
    _log(f"REFRAME {entry['id']} ({run_id}): campaign review's brief registered as {new_id} "
         f"(ready, origin {orch.CAMPAIGN_REVIEW_ORIGIN}, brief={rel}); decide-next picks the next run.")
    return True


def _register_from_cli(brief: Path, priority: int, notes: str) -> int:
    """The `register` sub-command. E-059 S2b (S1 §7, decision 7): a brief
    registered while decide_next is on starts `brief_status: open` (R2 may ask
    step 1a for more of it). Flag off: exactly the call made before.

    E-061 C1.5: reads decide_next's OWN value (strict: a non-bool still raises
    here), not its prerequisite chain. A misconfigured prerequisite used to
    crash `register`; it is now refused where every flag is checked -- the
    launch pre-flight in process_once, a classified pause naming the flag."""
    if orch._strict_orchestrator_flag("decide_next"):
        return register_hypothesis(brief, priority, notes, extra={"brief_status": "open"})
    return register_hypothesis(brief, priority, notes)


def run_forever(once: bool = False):
    while True:
        keep_going = process_once()
        if once or not keep_going:
            break


# ---------------------------------------------------------------------------
# Dry-run verification (no LLM spend, zero footprint on real campaign state)
# ---------------------------------------------------------------------------

# Both mean "the wishlist check caught the family": `wishlist_trigger` when its
# predicate evaluated false, `wishlist_trigger_data_gap` when it has no machine
# predicate yet (_hard_pause_reason). A predicate that evaluates true does not pause.
DRY_RUN_WISHLIST_PAUSE_REASONS = ("wishlist_trigger", "wishlist_trigger_data_gap")


def _dry_run_wishlist_probe(dry_run_dir: Path) -> str:
    """The dry run's wishlist self-test. Writes a synthetic reframe naming the
    first gating (feed) wishlist family into dry_run_dir and checks the
    campaign detects it. Returns the line to log; raises AssertionError when
    the family is not detected. D-052: only feed_wishlist names gate, so the
    probe uses a feed -- whose predicate may be absent (data_gap pause),
    false (trigger pause) or true (no pause); all three prove detection."""
    names = _gating_wishlist_names()
    if not names:
        return "wishlist-trigger probe skipped: no gating (feed) wishlist entries"
    probe_family = names[0]
    review = {
        "recommendation": "reframe",
        "recommendation_rationale": f"Testing {probe_family} looks promising now.",
        "next_research_question": {"strategy_domain": probe_family},
    }
    orch.save_yaml(dry_run_dir / "artifacts" / "campaign_review.yaml", review)
    if _check_wishlist_trigger(review) != probe_family:
        raise AssertionError(f"synthetic wishlist-trigger recommendation was not detected: "
                             f"{probe_family!r} not matched")
    state = orch.load_yaml(dry_run_dir / "pipeline_state.yaml")
    pause = _hard_pause_reason(dry_run_dir, state)
    fired = evaluate_wishlist_predicate(probe_family)["result"] == "true"
    if fired:
        if pause is not None and pause[0] in DRY_RUN_WISHLIST_PAUSE_REASONS:
            raise AssertionError(f"wishlist predicate for {probe_family!r} fired, but the run "
                                 f"still paused: {pause}")
        return f"wishlist-trigger classification OK: {probe_family!r} detected, predicate fired (no pause)"
    if pause is None or pause[0] not in DRY_RUN_WISHLIST_PAUSE_REASONS:
        raise AssertionError(f"synthetic wishlist-trigger recommendation was not detected: {pause}")
    return f"wishlist-trigger classification OK: detected reason={pause[0]!r} ({pause[1]})"


def dry_run_verify():
    _log("=== DRY RUN: verifying queue -> launch -> pause wiring (no LLM spend) ===", dry_run=True)

    reconcile_orphans()  # A3: read-only, always logs exactly one line (see its own docstring)

    queue = _load_queue()
    entry = _select_entry(queue["queue"])
    if entry is None:
        # K4 rider (2026-07-13): parity with process_once()'s own graceful
        # "Queue exhausted" handling -- an all-terminal queue (every entry
        # done/blocked_on_*) is a legitimate, informative outcome, not an
        # assertion failure. Previously raised AssertionError here, which
        # is indistinguishable from a real wiring defect.
        _log("DRY RUN: no ready/in_progress entry — nothing to verify; queue is all-terminal",
             dry_run=True)
        return
    _log(f"queue: selected entry '{entry['id']}' (status={entry['status']}, "
         f"brief={entry['brief_path']})", dry_run=True)

    # B1/B2-non-regression: classify via the SAME function process_once() uses,
    # so a broken refinement_brief_path is caught before a real launch. This
    # does not achieve B2's full dry-run/process_once branch parity (the
    # plain "continue" branch still isn't simulated at all) -- see design
    # note section 7.
    action = _next_action_for_entry(entry)
    _log(f"classified next action for '{entry['id']}': {action!r}", dry_run=True)

    brief_path = ROOT / entry["brief_path"]
    brief = _parse_brief_frontmatter(brief_path)
    _log(f"brief frontmatter parsed OK: strategy_domain={brief['strategy_domain']}, "
         f"market_universe={brief['market_universe']}", dry_run=True)

    dry_run_id = "run_dryrun_verify"
    dry_run_dir = ROOT / "runs" / dry_run_id
    if dry_run_dir.exists():
        shutil.rmtree(dry_run_dir)
    try:
        setup_run(dry_run_id)
        _materialize_run(dry_run_id, brief)
        rb_path = dry_run_dir / "artifacts" / "research_brief.yaml"
        if not rb_path.exists():
            raise AssertionError("research_brief.yaml was not written")
        pr_path = dry_run_dir / "artifacts" / "pre_registration.yaml"
        has_pr = pr_path.exists()
        _log(f"setup_run + brief materialization OK: {rb_path.relative_to(ROOT)} written"
             f"{', pre_registration.yaml written' if has_pr else ' (brief has no machine_constraints)'}",
             dry_run=True)

        if action == "refinement_brief":
            rb_source = ROOT / entry["refinement_brief_path"]
            rb_brief = _parse_refinement_brief_yaml(rb_source)
            _materialize_refinement_run(dry_run_id, rb_brief, rb_source)
            verbatim_path = dry_run_dir / "artifacts" / "user_brief_verbatim.yaml"
            if not verbatim_path.exists():
                raise AssertionError("user_brief_verbatim.yaml was not written")
            _log(f"refinement-brief materialization OK: {verbatim_path.relative_to(ROOT)} written "
                 f"(checksum recorded in pre_registration.yaml)", dry_run=True)

        # Simulate a normal terminal outcome (no LLM calls) — prove terminal
        # classification does NOT misfire as a pause.
        orch.update_state(path=dry_run_dir, pending_stage="completed_rejected", status="rejected")
        state = orch.load_yaml(dry_run_dir / "pipeline_state.yaml")
        pause = _hard_pause_reason(dry_run_dir, state)
        if pause is not None:
            raise AssertionError(f"synthetic normal-terminal state was misclassified as a pause: {pause}")
        _log("terminal-state classification OK: pending_stage=completed_rejected -> "
             "no pause, queue would advance", dry_run=True)

        # Simulate a no_signal_artifact hard pause — prove halt-and-do-not-advance.
        orch.update_state(path=dry_run_dir, pending_stage="human_pause", status="paused_for_human",
                           flags={"no_signal_artifact_flagged": True})
        state = orch.load_yaml(dry_run_dir / "pipeline_state.yaml")
        pause = _hard_pause_reason(dry_run_dir, state)
        if pause is None or pause[0] != "no_signal_artifact":
            raise AssertionError(f"synthetic no_signal_artifact pause was not detected: {pause}")
        _log(f"hard-pause classification OK: detected reason={pause[0]!r}", dry_run=True)

        # Simulate a wishlist-trigger reframe recommendation — proves this check
        # independently of the status-based pause detection above.
        _log(_dry_run_wishlist_probe(dry_run_dir), dry_run=True)

    finally:
        shutil.rmtree(dry_run_dir, ignore_errors=True)
        generated = ROOT / "protocols" / f"{dry_run_id}_generated.json"
        if generated.exists():
            generated.unlink()

    _log("cleanup complete — no real run_ids, campaign_state.yaml, or campaign_queue.yaml "
         "were touched.", dry_run=True)
    _log("=== DRY RUN PASSED ===", dry_run=True)


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multi-run campaign entry point (thin wrapper over run_phase1_research.py)."
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Verify queue->launch->pause wiring with zero LLM spend, then exit.")
    parser.add_argument("--once", action="store_true",
                        help="Process a single queue step (one launch/continue/advance), then exit.")
    parser.add_argument("--resume", action="store_true",
                        help="Resume a campaign halted at a hard pause, after the human has resolved it.")
    parser.add_argument("--unpark", metavar="ENTRY_ID",
                        help="Slice 6c S2c: restore a parked entry (paused:waiting_for_component|"
                             "data) once the component or data exists; sets it ready, then exits.")
    subparsers = parser.add_subparsers(dest="command")
    register_parser = subparsers.add_parser(
        "register",
        help="B15: register a fully-authored brief as a new, schedulable queue entry."
    )
    register_parser.add_argument("--brief", required=True, type=Path,
                                  help="Path to the brief .md (frontmatter-format).")
    register_parser.add_argument("--priority", required=True, type=int,
                                  help="Queue priority (lower sorts first, matching _select_entry).")
    register_parser.add_argument("--notes", required=True,
                                  help="One-line-or-more notes recorded on the queue entry.")
    args = parser.parse_args()

    if Path(".").resolve() != ROOT:
        print(f"This must be run with CWD = {ROOT} (matches run_phase1_research.py's own "
              f"ROOT=Path('.') convention). Current CWD: {Path('.').resolve()}. "
              f"cd into strategy-research/ and retry.")
        sys.exit(1)

    if args.command == "register":
        sys.exit(_register_from_cli(args.brief, args.priority, args.notes))

    if args.dry_run:
        dry_run_verify()
        sys.exit(0)

    if args.unpark:
        # Takes and releases the campaign lock itself (refused while a campaign
        # runs); relaunch afterwards to continue the queue.
        sys.exit(0 if _unpark_entry(args.unpark) else 1)

    if args.resume:
        if not resume_paused_entry(_load_queue()):
            sys.exit(1)

    # E-011 S1b: only one real campaign run_forever() loop may run at a time
    # on a shared host (--dry-run and `register` never reach this point, so
    # they are correctly never gated by it). See tools/campaign_lock.py for
    # the design and why this is deliberately not full concurrent-write
    # safety (that's E-051).
    lock_path = campaign_lock.lock_path_for(orch.CAMPAIGN_STATE_PATH)
    try:
        campaign_lock.acquire(lock_path)
    except campaign_lock.CampaignLockHeld as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
    try:
        run_forever(once=args.once)
    finally:
        campaign_lock.release(lock_path)
