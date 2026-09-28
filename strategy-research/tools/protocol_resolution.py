"""
protocol_resolution.py — the ONE shared protocol-selection resolver.

Extracted 2026-09-11 (E-054 Layer 2) from
strategy-research/workflow/run_phase1_research.py::_resolve_protocol_path,
which remains the orchestrator's own entry point (now a thin delegator to
`resolve_protocol_path` below — see that function's docstring). This module
exists so a SECOND consumer (E-054's data-availability gate) can resolve
"which protocol file will `signal_prescreen`/`protocol_execution` actually
run against" without duplicating the 4-branch decision logic — duplicating it
is exactly the class of silent-drift bug this project has hit before (E-033
S1's `validation.conditions` field silently failing to reach
`backtest_specification` because the routing/handoff contract didn't carry
it; see E-054's own Phase 1 characterization, 2026-09-11).

Deliberately dependency-light: no `claude_agent_sdk` / `google-genai` import.
Those are workflow-orchestrator-only dependencies (declared in
strategy-research/config/requirements-mac.txt, absent from
trading-bot/requirements.txt) — importing run_phase1_research.py directly
from a script that must run under the trading-bot venv (to reach
`data.data_manager.DataManager`, as E-054 Layer 2 does) would fail at import
time on a host that only has the trading-bot venv provisioned. This module
has no such dependency and imports cleanly under either venv.

Scope note on `_load_small_yaml`: it uses plain `yaml.safe_load`, with none
of `run_phase1_research.py::load_yaml`'s LLM-output repair pass. That is a
deliberate, bounded simplification, not a behavioral gap: every file this
module reads (`run_context.yaml`, `campaign_state.yaml`) is machine-written
exclusively by that orchestrator's own `save_yaml` (temp-file + atomic
`os.replace`) — never LLM-authored — so the repair path is unreachable for
these specific files as a matter of provenance, not assumption.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Optional

import yaml


class UngatedProtocolError(ValueError):
    """Mirrors run_phase1_research.py's UngatedProtocolError. Kept as a
    separate class (not a re-export) so this module never imports that
    heavy orchestrator file — see module docstring. Any caller that needs
    interop with the orchestrator's own class should catch ValueError, or
    catch this class by name and re-wrap (run_phase1_research.py does this
    at its own delegation call site)."""


# C7-EXT-R / D-3 (run_phase1_research.py): the exact abolished generic
# promotion block, byte-for-byte, kept in sync deliberately — see that
# file's own `_GENERIC_PROMOTION` comment for the full history.
_GENERIC_PROMOTION = {
    "median_sharpe_gt": 0,
    "max_abs_drawdown_pct_lt": 30,
    "min_trade_count_gte": 20,
    "kill_median_sharpe_lt": -1,
}


def promotion_is_generic(promotion) -> bool:
    """True when a promotion block is byte-equal to the abolished code default."""
    return isinstance(promotion, dict) and dict(promotion) == _GENERIC_PROMOTION


def _load_small_yaml(path: Path) -> dict:
    """Load a small, machine-written YAML file. See module docstring for why
    this deliberately skips the LLM-repair pass `load_yaml` has."""
    path = Path(path)
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_campaign_data_policy(policy_path: Path | None = None) -> dict:
    """The ONE shared reader for config/campaign_data_policy.yaml (E-061
    C1.6/C1.7 second-round code-review fix, dedup). Previously two
    independent implementations existed: tools/run_protocol.py's own
    `_load_campaign_data_policy()` (whole file) and
    tools/verdict_criteria_evaluator.py's `_load_campaign_data_policy_eras()`
    (opened and parsed the same file a second time, independently, just to
    read `eras`). Both are now thin delegators to this function (and to
    `load_policy_eras` below).

    Fail-SOFT (returns {} if the file is absent), matching both former
    implementations' own behaviour for this specific, additive use --
    callers that genuinely require the file to exist do their own loud
    presence check (e.g. run_phase1_research.py::_load_holdout_range,
    which is a hard dependency for holdout-boundary safety, not an optional
    read)."""
    p = Path(policy_path) if policy_path else (
        Path(__file__).resolve().parent.parent / "config" / "campaign_data_policy.yaml")
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_policy_eras(policy_path: Path | None = None) -> list:
    """The `eras` list from `load_campaign_data_policy` above -- the ONE
    shared accessor both tools/run_protocol.py (via its own
    `_load_campaign_data_policy()`, itself now delegating here) and
    tools/verdict_criteria_evaluator.py use."""
    return load_campaign_data_policy(policy_path).get("eras") or []


# E-061 C1.6/C1.7 second-round code-review fix: memoizes era_id_for_timestamp's
# LOOKUP (which era a given calendar day belongs to), keyed on the already-
# normalized "YYYY-MM-DD" string plus id(eras) -- NOT on the raw `ts` passed
# in, so two different representations of the same UTC day (a string, a
# tz-aware Timestamp that normalizes to it, ...) share one cache entry. A
# plain dict, not functools.lru_cache: `eras` is a list of dicts and
# therefore unhashable, so identity (id()) stands in for it -- correct here
# because a caller either reuses the SAME eras list object across many calls
# (the common case: loaded once per process) or passes a fresh one each time
# (a synthetic test list), in which case a stale id() simply never gets a
# cache hit rather than returning a wrong answer. Intentionally unbounded:
# one process's total distinct (era-list-identity, calendar-day) pairs is
# bounded by the campaign's own date range, at most a few thousand entries.
_ERA_LOOKUP_CACHE: dict[tuple[int, str], str] = {}


def era_id_for_timestamp(ts, eras: list) -> str:
    """The ONE shared implementation (E-061 C1.6 code-review fix), replacing
    two independent copies that had drifted (tools/run_protocol.py and
    tools/verdict_criteria_evaluator.py, both originally A8.5.1a: map a bar
    timestamp to its era_id per campaign_data_policy.yaml's `eras` list).
    Returns 'era_unmapped' if the timestamp falls outside every declared era
    (should not happen for in-policy data, but must not crash).

    campaign_data_policy.yaml's last era (era_2026_h2_forward_recorded) has an
    open-ended upper bound, `range: [2026-07-26, null]`; a naive `lo <= d <= hi`
    raises TypeError against that None (`str <= None` is unorderable in Python
    3). No era currently declares a null LOWER bound, but the same hazard
    applies symmetrically, so both sides are guarded.

    Simplified from the two former per-file implementations' explicit
    None-branching (an `if lo is None / if hi is None / if lo is None and hi
    is None` cascade, each returning early) to a single boolean expression per
    era: `(lo is None or lo <= d) and (hi is None or d <= hi)`. This is
    behaviourally identical for all four cases -- `lo is None` alone makes the
    first clause vacuously True (any `d` matches from below), `hi is None`
    alone does the same for the second clause (any `d` matches from above),
    both None makes the whole expression True unconditionally, and both set
    reduces to the original `lo <= d <= hi` -- see
    test_protocol_resolution_era_id.py's boundary/None/gap cases for the
    executed proof, not just this docstring's claim.

    TIMESTAMP NORMALIZATION (second-round code-review fix). A tz-AWARE
    timestamp is converted to UTC before its calendar date is taken --
    campaign_data_policy.yaml's era boundaries are UTC-anchored bar dates, so
    e.g. a 02:00 Asia/Kolkata (UTC+5:30) reading of an era's first calendar
    day must resolve by its UTC date (still the PREVIOUS day, 20:30 UTC),
    not its local one, or a bar just after UTC midnight silently attributes
    to the wrong era for any caller passing tz-aware data (see
    test_protocol_resolution_era_id.py's tz-aware tests, which compute their
    probe dates from the policy file at runtime rather than using a literal
    one here). A tz-NAIVE timestamp is treated AS ALREADY UTC --
    UNCHANGED from every prior version of this function: every real caller in
    this codebase (bar timestamps, ISO date strings from the policy file
    itself) is naive-and-implicitly-UTC, so this is a pin, not a new
    decision. A bare int/float (e.g. an epoch-ms integer) is REJECTED with
    ValueError rather than silently guessed at -- pandas' own
    `Timestamp(int)` unit inference (nanoseconds by default, ms/s only with
    an explicit `unit=`) makes a bare number ambiguous, and an ambiguous
    value feeding an era classification is exactly the class of silent-
    default bug this module exists to avoid (see timeframe.py::
    timeframe_seconds's identical philosophy)."""
    if isinstance(ts, bool) or isinstance(ts, (int, float)):
        raise ValueError(
            f"era_id_for_timestamp: a bare number ({ts!r}) is ambiguous -- pandas "
            f"infers its unit inconsistently (nanoseconds by default). Pass an ISO "
            f"date string, a datetime/Timestamp, or another type pandas parses "
            f"unambiguously, not a raw int/float."
        )
    import pandas as pd
    parsed = pd.Timestamp(ts)
    if parsed.tzinfo is not None:
        parsed = parsed.tz_convert("UTC")
    d = parsed.strftime("%Y-%m-%d")

    cache_key = (id(eras), d)
    cached = _ERA_LOOKUP_CACHE.get(cache_key)
    if cached is not None:
        return cached

    for era in eras:
        lo, hi = era["range"]
        if (lo is None or lo <= d) and (hi is None or d <= hi):
            _ERA_LOOKUP_CACHE[cache_key] = era["era_id"]
            return era["era_id"]
    _ERA_LOOKUP_CACHE[cache_key] = "era_unmapped"
    return "era_unmapped"


def assert_promotion_ratified(protocol_path: Path) -> None:
    """Byte-for-byte port of run_phase1_research.py::_assert_promotion_ratified.
    See that function's own docstring for the full G7/D-3 history."""
    try:
        with open(protocol_path, "r", encoding="utf-8") as fh:
            protocol_obj = json.load(fh)
    except (OSError, ValueError):
        return  # existence/parse failures are other checks' business, not this one
    if not isinstance(protocol_obj, dict):
        return

    promotion = protocol_obj.get("promotion")
    if not promotion_is_generic(promotion):
        return

    provenance = protocol_obj.get("promotion_provenance") or {}
    if isinstance(provenance, dict) and provenance.get("ratified_by"):
        return

    raise UngatedProtocolError(
        f"[G7/D-3] {protocol_path.name} carries the abolished generic promotion "
        f"block {_GENERIC_PROMOTION} with no `promotion_provenance.ratified_by`. "
        f"These four numbers came from a code default, not from any brief -- they "
        f"are the same unregistered '30% DD bar' the XS_momentum verdict was "
        f"argued against. Refusing to run a verdict-bearing protocol against them. "
        f"Either pre-register real thresholds for this hypothesis, or add "
        f"promotion_provenance: {{ratified_by, ratified_at}} to {protocol_path.name} "
        f"to state on the record that these values were adopted deliberately."
    )


def resolve_protocol_path(
    run_dir: Path,
    run_id: str,
    protocols_root: Path,
    campaign_state: Optional[dict] = None,
    on_stale_escalation: Optional[Callable[[], None]] = None,
) -> Path:
    """
    The ONE shared protocol-selection resolver. Byte-for-byte port of the
    decision logic in run_phase1_research.py::_resolve_protocol_path (K3,
    B3+B10, C7-EXT-R/D-3) — see that function's own docstring for the full
    design history. Four branch classes: replication_diagnostic;
    protocol-GENERATED forced_diagnostic; protocol_ref-PINNED; and the
    claim-checked last_escalation fallback (B10), which hard-fails instead of
    silently reusing stale campaign-wide state unless this run is that
    escalation's own claimed consumer.

    Parameterized (rather than reading orchestrator globals directly) so a
    second caller outside the orchestrator process — E-054 Layer 2's
    data-availability gate — gets the IDENTICAL resolution without importing
    run_phase1_research.py's heavy LLM-SDK dependencies.

    Args:
        run_dir: the run's root directory (contains artifacts/, pipeline_state.yaml).
        run_id: this run's id, checked against a claimed last_escalation.
        protocols_root: directory protocol filenames resolve relative to
            (the orchestrator's `ROOT / "protocols"`).
        campaign_state: the loaded campaign_state.yaml dict (or None/{} if
            absent) — the B10 fallback reads `last_escalation` from this.
        on_stale_escalation: optional zero-arg callback invoked BEFORE the
            B10 hard-fail raises (the orchestrator uses this to flag
            `stale_escalation_unclaimed` on pipeline_state.yaml; a caller
            outside the pipeline state machine, like the data-availability
            gate, can leave this None).

    Raises:
        UngatedProtocolError: forced_diagnostic with no `protocol` named, or
            (via assert_promotion_ratified) a selected protocol carries the
            abolished generic promotion block unratified.
        RuntimeError: protocol_ref_pinned with no `protocol` key (malformed
            pin state), or the B10 fallback with no claimed last_escalation.
    """
    run_dir = Path(run_dir)
    protocols_root = Path(protocols_root)
    artifacts = run_dir / "artifacts"
    run_ctx_path = artifacts / "run_context.yaml"
    run_ctx = _load_small_yaml(run_ctx_path)
    run_type = run_ctx.get("run_type", "")

    def _selected(path: Path) -> Path:
        assert_promotion_ratified(path)
        return path

    if run_type == "replication_diagnostic":
        return _selected(protocols_root / "baseline_v1.json")

    if run_type == "forced_diagnostic":
        proto_name = run_ctx.get("protocol")
        if not proto_name:
            raise UngatedProtocolError(
                f"[G7/D-3] run {run_id}: run_context.yaml declares "
                f"run_type=forced_diagnostic but names no `protocol`. Refusing to "
                f"default to baseline_v1.json -- a diagnostic that does not say what "
                f"it is running against silently inherits generic thresholds. Name "
                f"the protocol explicitly in run_context.yaml."
            )
        return _selected(protocols_root / proto_name)

    if run_type == "protocol_ref_pinned":
        proto_name = run_ctx.get("protocol")
        if not proto_name:
            raise RuntimeError(
                f"[K3] run_context.yaml declares run_type=protocol_ref_pinned but has no "
                f"'protocol' key -- malformed pin state for {run_id}."
            )
        return _selected(protocols_root / proto_name)

    # B10 fallback: campaign-wide last_escalation, claim-checked (§4).
    campaign = campaign_state or {}
    last_escalation = campaign.get("last_escalation") or {}
    claimed_by = last_escalation.get("claimed_by_run")
    protocol_path_str = last_escalation.get("protocol_path")
    if protocol_path_str and claimed_by == run_id:
        return _selected(Path(protocol_path_str))

    if on_stale_escalation is not None:
        on_stale_escalation()
    raise RuntimeError(
        f"[B10] No run_context.yaml override and no machine_constraints.protocol_ref "
        f"for {run_id}, and campaign_state.last_escalation "
        f"(protocol_path={protocol_path_str!r}) is either empty or claimed by a "
        f"different run ({claimed_by!r}) -- refusing to silently run against stale, "
        f"unrelated campaign-wide state. Pin this run's protocol explicitly via "
        f"machine_constraints.protocol_ref in pre_registration.yaml."
    )
