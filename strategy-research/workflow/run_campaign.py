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
import hashlib
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import run_phase1_research as orch  # noqa: E402  (path insert must precede this)
import campaign_lock  # noqa: E402  (E-011 S1b, single-writer campaign launch lock)
import record_schema  # noqa: E402  (closed record schema, see _save_queue)
import verdict_criteria_evaluator as vce  # noqa: E402  (G6, see _save_queue)
from setup_run import setup_run  # noqa: E402

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
        return "fresh_launch"
    return "continue"


# ---------------------------------------------------------------------------
# Brief materialization
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Phase 1.3 (docs/CAMPAIGN_PROGRAM.md): venue/product registration-rule mechanism.
# Single source of truth: config/venue_tradability.yaml. Consumed by
# _materialize_run() below to auto-flag research_only on any brief whose
# declared venue+product isn't tradable==true, or whose venue/product is
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


def _venue_product_tradable(venue, product) -> bool:
    """False if venue/product is undeclared, the (venue, product) pair is
    absent from the table, or its tradable field isn't literal True --
    "unconfirmed" and False both resolve to False, only True passes."""
    if not venue or not product:
        return False
    table = _load_venue_tradability()
    entry = table["venues"].get(venue, {}).get(product)
    if entry is None:
        return False
    return entry.get("tradable") is True


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
    # to research_only=True via _venue_product_tradable's own fail-closed default
    # (still exercised directly by _materialize_run for any caller that bypasses
    # this parser, e.g. test_venue_tradability.py's direct-dict tests). No longer
    # load-bearing for holdout safety -- S3's affirmative research_only is False
    # check already closes that gap -- this is belt-and-braces at registration
    # time, which is what the rule was originally written to require.
    for required in (
        "strategy_domain", "market_universe", "timeframe", "research_goal",
        "venue", "product",
    ):
        if not data.get(required):
            raise ValueError(f"{brief_path}: frontmatter missing required field '{required}'.")
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


def _materialize_run(run_id: str, brief: dict):
    """Write runs/<run_id>/artifacts/research_brief.yaml (and pre_registration.yaml
    if the brief carries machine_constraints) into an already-scaffolded run dir."""
    run_dir = ROOT / "runs" / run_id
    artifacts = run_dir / "artifacts"
    research_brief = {k: v for k, v in brief.items() if k != "machine_constraints"}
    venue = brief.get("venue")
    product = brief.get("product")
    tradable = _venue_product_tradable(venue, product)
    research_brief["research_only"] = not tradable
    _log(f"VENUE-CHECK {run_id}: venue={venue!r} product={product!r} tradable={tradable} "
         f"research_only={not tradable}")
    orch.save_yaml(artifacts / "research_brief.yaml", research_brief)

    machine_constraints = brief.get("machine_constraints")
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
        }
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

def register_hypothesis(brief_path: Path, priority: int, notes: str) -> int:
    """Parse `brief_path` via the EXISTING _parse_brief_frontmatter (propagates
    its own ValueError, unmodified, on a malformed brief); derive the queue id
    from the brief's filename stem; refuse (one log line, nonzero return) if
    that id already exists in the queue; otherwise append an entry mirroring
    the H-041-C-v2 entry's own field set (id, brief_path, status: ready,
    priority, source: operator_ratified, relation: new_registration, notes,
    run_ids: [], no outcome key) via the EXISTING _load_queue/_save_queue
    pair. Emits exactly one log line, success or refusal, never zero."""
    brief_path = Path(brief_path)
    try:
        _parse_brief_frontmatter(brief_path)
    except ValueError as err:
        _log(f"REGISTER REFUSED: malformed brief {brief_path}: {err}")
        return 1

    new_id = brief_path.stem
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
        "status": "ready",
        "priority": priority,
        "source": "operator_ratified",
        "relation": "new_registration",
        "notes": notes,
        "run_ids": [],
    }
    queue["queue"].append(entry)
    _save_queue(queue)
    _log(f"REGISTER: queue entry '{new_id}' appended (brief={brief_rel_str}, "
         f"priority={priority}, status=ready).")
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
    for name in _wishlist_family_names():
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
    # engineering failure.
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
        return _classify_human_pause(run_dir, state), ""

    return None


def _append_halt_history(run_dir: Path, state: dict, reason: str, detail: str = "",
                         quarantine: dict | None = None) -> None:
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
    which continues from pipeline_state.yaml's own pending_stage."""
    paused = [e for e in queue["queue"] if str(e.get("status", "")).startswith("paused:")]
    if not paused:
        print("No paused queue entry found — nothing to resume.")
        return False
    entry = paused[0]
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
        entry["status"] = "in_progress"
        _save_queue(queue)
        _log(f"RESUME {entry['id']} / {run_id}: data_block_hitl — invoking resume_pipeline().")
        orch.resume_pipeline(run_id)
        return True

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
    entry["status"] = "in_progress"
    _save_queue(queue)
    _log(f"RESUME {entry['id']} / {run_id}: resolution confirmed for '{reason}', "
         f"resuming queue processing.")
    return True


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
        lines.append(f"| {e['id']} | {e['status']} | {run_ids_str} | {e.get('outcome') or '-'} |")
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
    for _run_id, history in histories:
        for i, record in enumerate(history):
            if "quarantine" in record:
                auto_recovered += 1
            else:
                escalated += 1
            # The R4 population, computed with the SAME predicate the decision uses
            # (_repeat_quarantine), so the instrument and the decision cannot drift.
            if _repeat_quarantine({"halt_history": history[:i]}, record.get("reason")):
                repeat_pairs += 1

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
        "outcomes": {
            "auto_recovered": auto_recovered,
            "escalated": escalated,
            "halt_history_records": auto_recovered + escalated,
            "repeat_quarantine_escalations": repeat_pairs,
            "denominator_note": ("halt_history across every run on disk, which covers "
                                 "both quarantined and escalated halts. Does not equal "
                                 "halts.total."),
        },
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

def _schedulability_block_enabled() -> bool:
    """E-031 S2 gate. False (no file written, no behavior change) when the
    key, the section, or the config file is absent -- same silence-is-never-
    a-green-light rule as _quarantine_enabled() just above."""
    path = ROOT / "config" / "campaign_config.yaml"
    if not path.exists():
        return False
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    section = ((cfg.get("orchestrator") or {}).get("schedulability_block") or {})
    return bool(section.get("enabled", False))


# Statuses that are NOT "blocked" for schedulability purposes. `ready` and
# `in_progress` are schedulable; `done` and `superseded` are TERMINAL (both are
# schema-legal per _QUEUE_STATUS_RE). Review fix 2, 2026-08-26: `superseded`
# was previously bucketed as blocked, emitting a phantom blocker row.
_SCHEDULABILITY_NON_BLOCKED_STATUSES = ("ready", "in_progress", "done", "superseded")

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
    later ledger item -- this is only the detection half."""
    return (ROOT / "runs" / run_id / "ORPHANED_README.md").exists()


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


def process_once() -> bool:
    """Runs exactly one launch/continue/advance step. Returns True if the
    caller should keep looping, False if the campaign is done or halted."""
    reconcile_orphans()  # A3: read-only, logs only newly-unexpected orphans

    # E-031 S2. Written BEFORE the queue-exhausted check below on EVERY step
    # (not only when exhausted) -- closing E-030's own measured blind spot
    # (all four _write_loop_health() call sites sit after a non-None
    # _select_entry() result). Flag-off: no-op, byte-identical to before
    # this feature existed.
    schedulability_enabled = _schedulability_block_enabled()
    if schedulability_enabled:
        _write_schedulability()

    queue = _load_queue()
    entry = _select_entry(queue["queue"])
    if entry is None:
        _log("Queue exhausted — no ready or in_progress entries remain.")
        return False

    action = _next_action_for_entry(entry)

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

        brief_path = ROOT / entry["refinement_brief_path"]
        brief = _parse_refinement_brief_yaml(brief_path)
        child_id = _next_new_run_id()
        setup_run(child_id)
        _materialize_refinement_run(child_id, brief, brief_path)
        entry["run_ids"].append(child_id)
        entry["refinement_brief_consumed_for"] = entry["refinement_brief_path"]
        _save_queue(queue)
        _log(f"REFINEMENT-BRIEF {entry['id']} -> {child_id} (brief={entry['refinement_brief_path']})")
        run_id = child_id
    elif action == "fresh_launch":
        brief_path = ROOT / entry["brief_path"]
        brief = _parse_brief_frontmatter(brief_path)
        run_id = _next_new_run_id()
        setup_run(run_id)
        _materialize_run(run_id, brief)
        entry["run_ids"] = [run_id]
        entry["status"] = "in_progress"
        _save_queue(queue)
        _log(f"LAUNCH {entry['id']} -> {run_id} (brief={entry['brief_path']})")
    else:
        run_id = entry["run_ids"][-1]

    run_dir = ROOT / "runs" / run_id
    before_splits = _snapshot_hypothesis_splits()
    orch.run_loop(run_id)
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

    state = orch.load_yaml(run_dir / "pipeline_state.yaml")
    _log_transition(entry, run_id, state)

    pause = _hard_pause_reason(run_dir, state)
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
                _write_loop_health()  # E-030 S3 — see the note at the first call site
                if schedulability_enabled:  # E-031 S2 — same end-of-branch placement
                    _write_schedulability()
                return True
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
    entry["outcome"] = pending or state.get("status")
    _save_queue(queue)
    _regenerate_summary(queue)
    _log(f"DONE {entry['id']} ({run_id}) -> {entry['outcome']}")
    _write_loop_health()  # E-030 S3 — see the note at the first call site
    if schedulability_enabled:  # E-031 S2 — same end-of-branch placement
        _write_schedulability()
    return True


def run_forever(once: bool = False):
    while True:
        keep_going = process_once()
        if once or not keep_going:
            break


# ---------------------------------------------------------------------------
# Dry-run verification (no LLM spend, zero footprint on real campaign state)
# ---------------------------------------------------------------------------

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
        names = _wishlist_family_names()
        probe_family = names[0] if names else "daily_timeframe_er_overlay"
        cr_path = dry_run_dir / "artifacts" / "campaign_review.yaml"
        orch.save_yaml(cr_path, {
            "recommendation": "reframe",
            "recommendation_rationale": f"Testing {probe_family} looks promising now.",
            "next_research_question": {"strategy_domain": probe_family},
        })
        state = orch.load_yaml(dry_run_dir / "pipeline_state.yaml")
        pause = _hard_pause_reason(dry_run_dir, state)
        if pause is None or pause[0] != "wishlist_trigger":
            raise AssertionError(f"synthetic wishlist-trigger recommendation was not detected: {pause}")
        _log(f"wishlist-trigger classification OK: detected family={pause[1]!r}", dry_run=True)

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
        sys.exit(register_hypothesis(args.brief, args.priority, args.notes))

    if args.dry_run:
        dry_run_verify()
        sys.exit(0)

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
