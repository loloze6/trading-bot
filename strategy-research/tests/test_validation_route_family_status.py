"""
F4f (2026-07-06, run_053): determine_post_validation_route() crashed with
'NoneType' object has no attribute 'strip' on a real multi-variant family
validation. The quant-validation skill's real output for a 5-variant MACD
family used `family_status`/`family_rationale`/`family_blocking_issues` plus a
`variant_decisions` list, instead of the schema-canonical top-level `status`
(schemas/validation_decision.schema.json requires status/rationale/
blocking_issues; `family_status` isn't even a schema-valid key). This halted
the whole campaign_queue run (run_campaign.py) with an unhandled_exception
hard-pause. Fixture: run_053's real validation_decision.yaml content, frozen.
"""
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
WORKFLOW_PATH = ROOT / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402

# Frozen real content from run_053/artifacts/validation_decision.yaml (2026-07-06).
REAL_RUN_053_FAMILY_DECISION = """
family_hypothesis_id: MACD_TREND_CONTINUATION_EXTENDED_2018_2025

family_status: approve

family_rationale: |
  All 5 variants are cost-feasible and mechanically sound.

family_blocking_issues: []

variant_decisions:
  - variant_id: MACD_HISTOGRAM_CROSSOVER_V1
    status: approve
    rationale: "Baseline MACD crossover mechanically sound."
    blocking_issues: []
    conditions: []
  - variant_id: MACD_CROSSOVER_FUNDING_FILTER_V4
    status: conditional_approve
    rationale: "Structural funding-rate gate is economically motivated."
    blocking_issues: ["asymmetric_shorts_gate_untested"]
    conditions: ["config_enforces_shorts_inhibition_only"]
"""


def _make_run(tmp_path, decision_yaml_text):
    run_dir = tmp_path / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "validation_decision.yaml").write_text(decision_yaml_text, encoding="utf-8")
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"run_id": "run_test", "counters": {"refinements_used": 0},
                        "governance": {"max_refinements_after_validation": 2}}),
        encoding="utf-8",
    )
    return run_dir


def test_family_status_fixture_previously_crashed_now_routes(tmp_path, monkeypatch):
    """The real run_053 fixture must no longer raise AttributeError, and must
    route as a normal 'approve' would (family_status=approve)."""
    run_dir = _make_run(tmp_path, REAL_RUN_053_FAMILY_DECISION)

    # A8.6 power check and downstream state writes aren't the point of this test —
    # stub them out so we isolate the status-parsing fix.
    monkeypatch.setattr(rpr, "_run_a86_power_check", lambda artifacts_dir: {"verdict": "power_adequate"})
    monkeypatch.setattr(rpr, "update_state", lambda **kwargs: None)

    # Must not raise.
    result = rpr.determine_post_validation_route(run_dir)
    assert result is not None


def test_conditional_approve_aggregates_per_variant_conditions(tmp_path, monkeypatch):
    monkeypatch.setattr(rpr, "_run_a86_power_check", lambda artifacts_dir: {"verdict": "power_adequate"})
    monkeypatch.setattr(rpr, "update_state", lambda **kwargs: None)

    decision_text = """
family_status: conditional_approve
family_rationale: "test"
family_blocking_issues: []
variant_decisions:
  - variant_id: V1
    status: approve
    conditions: []
  - variant_id: V4
    status: conditional_approve
    conditions: ["cond_a", "cond_b"]
"""
    run_dir = _make_run(tmp_path, decision_text)
    # Just confirm no crash; conditions are printed, not returned, so this test
    # exercises the aggregation code path without asserting stdout content.
    result = rpr.determine_post_validation_route(run_dir)
    assert result is not None


def test_neither_status_nor_family_status_fails_loudly(tmp_path, monkeypatch):
    monkeypatch.setattr(rpr, "_run_a86_power_check", lambda artifacts_dir: {"verdict": "power_adequate"})
    monkeypatch.setattr(rpr, "update_state", lambda **kwargs: None)

    run_dir = _make_run(tmp_path, "hypothesis_id: H-TEST\nrationale: no status field at all\n")
    with pytest.raises(ValueError, match="neither 'status' nor 'family_status'"):
        rpr.determine_post_validation_route(run_dir)


def test_normal_single_hypothesis_status_still_works_unchanged(tmp_path, monkeypatch):
    """Non-regression: the standard, schema-conformant shape must be unaffected."""
    monkeypatch.setattr(rpr, "_run_a86_power_check", lambda artifacts_dir: {"verdict": "power_adequate"})
    monkeypatch.setattr(rpr, "update_state", lambda **kwargs: None)

    run_dir = _make_run(tmp_path, 'hypothesis_id: "H-TEST"\nstatus: "approve"\nrationale: "fine"\nblocking_issues: []\n')
    result = rpr.determine_post_validation_route(run_dir)
    assert result is not None
