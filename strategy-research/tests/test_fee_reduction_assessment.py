"""
Phase 1.4 (docs/ROADMAP.md) fee-reduction autopsy field regression tests,
2026-07-21.

Mirrors test_circuit_breaker_family_scoping.py's
test_component_execution_error_is_immune_to_the_breaker fixture style
(direct monkeypatch of rpr.ROOT/CAMPAIGN_STATE_PATH, hand-written
verdict_interpretation.yaml + pipeline_state.yaml, calling
determine_post_verdict_route directly) -- the lightest fixture that reaches
the mechanism_failure routing block. Uses status="kill" (hypothesis_verdict=
kill, lineage_routing=terminate) so each test short-circuits into the
terminal _route_kill path immediately after the routing block runs, the
same way the existing component_execution_error test short-circuits into
human_pause -- avoiding the much heavier carryover/KB-write/output-
verification fixture the non-terminal branches would need.

Unlike component_execution_error/regime_misattribution, a missing
fee_reduction_assessment does NOT pause the pipeline (see the code
comment at the call site) -- so these tests assert the WARNING TEXT via
capsys, not a route/state change.
"""
import sys
from pathlib import Path

import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr
from run_phase1_research import determine_post_verdict_route


def _write_fixture(tmp_path, root_cause: dict):
    run_dir = tmp_path / "runs" / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    interp = {
        "hypothesis_id": "X", "status": "kill", "hypothesis_family": "some_family",
        "proposed_change_dimension": "whatever",
        "root_cause": root_cause,
    }
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump(interp), encoding="utf-8"
    )
    (run_dir / "pipeline_state.yaml").write_text(yaml.safe_dump({
        "run_id": "run_test", "status": "running", "current_stage": "verdict_interpreter",
        "pending_stage": "verdict_interpreter", "completed_stages": [],
    }), encoding="utf-8")
    (tmp_path / "campaign_state.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")
    return run_dir


def test_fee_reduction_assessment_missing_emits_warning(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rpr, "ROOT", tmp_path)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")
    run_dir = _write_fixture(tmp_path, {
        "mechanism_failure": "signal_real_but_subscale_vs_costs",
        "supporting_evidence": "cost_drag_pct=180, corr=0.02",
    })

    next_stage = determine_post_verdict_route(run_dir, "run_test")

    captured = capsys.readouterr()
    assert "Phase 1.4" in captured.out
    assert "fee_reduction_assessment is missing" in captured.out
    # a completeness nudge, not a pipeline pause -- routing proceeds normally
    assert next_stage == "completed_rejected"


def test_fee_reduction_assessment_present_suppresses_warning(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rpr, "ROOT", tmp_path)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")
    run_dir = _write_fixture(tmp_path, {
        "mechanism_failure": "signal_real_but_subscale_vs_costs",
        "supporting_evidence": "cost_drag_pct=180, corr=0.02",
        "fee_reduction_assessment": {
            "has_fee_reduction_system": True,
            "candidate_system": "maker_only_execution",
            "registered_as": "briefs/some_cheap_variant.md",
        },
    })

    next_stage = determine_post_verdict_route(run_dir, "run_test")

    captured = capsys.readouterr()
    assert "Phase 1.4" not in captured.out
    assert next_stage == "completed_rejected"


def test_other_mechanism_failure_never_triggers_fee_reduction_warning(tmp_path, monkeypatch, capsys):
    """The warning is gated on mechanism_failure specifically -- a different
    value, even with no fee_reduction_assessment, must not fire it."""
    monkeypatch.setattr(rpr, "ROOT", tmp_path)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")
    run_dir = _write_fixture(tmp_path, {
        "mechanism_failure": "already_priced_in",
        "supporting_evidence": "edge_to_cost_ratio=0.36, not significant",
    })

    next_stage = determine_post_verdict_route(run_dir, "run_test")

    captured = capsys.readouterr()
    assert "Phase 1.4" not in captured.out
    assert next_stage == "completed_rejected"
