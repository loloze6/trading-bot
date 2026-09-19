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
