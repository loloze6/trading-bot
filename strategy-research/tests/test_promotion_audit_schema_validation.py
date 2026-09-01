"""CUL-14: promotion_audit.yaml must validate against promotion_audit.schema.json
on BOTH writers (pipeline `run_phase1_research._write_promotion_audit` and library
`deflate_sharpe.compute_promotion_audit`), across the happy and every degenerate DSR
path, after the schema declares the 5 previously-undeclared fields.

Also pins the `promotion_threshold_raw` value fix: the pipeline path must write the
computed E_max_SR (not the old hardcoded 0.0). The schema alone cannot catch this
(the field is typed number|null with no const), so a VALUE assertion is required.
"""

import json
import sys
from pathlib import Path

import pytest
import yaml

# jsonschema is an undeclared transitive (via mcp); skip cleanly in a leaned-out env
# rather than failing collection (D1 pending with Dorian).
jsonschema = pytest.importorskip("jsonschema")

TOOLS_PATH = Path(__file__).parent.parent / "tools"
WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
SCHEMA_PATH = Path(__file__).parent.parent / "workflow_artifacts" / "schemas" / "promotion_audit.schema.json"
sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(WORKFLOW_PATH))

import deflate_sharpe as ds  # noqa: E402
import run_phase1_research as rpr  # noqa: E402


def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _validate(audit: dict) -> None:
    """Raises jsonschema.ValidationError if the audit dict violates the schema."""
    jsonschema.validate(instance=audit, schema=_schema())


def _seed_state(path: Path, trials: list[dict], **extra) -> None:
    data: dict = {"trial_sharpes": [dict(t) for t in trials]}
    data.update(extra)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


def _run_pipeline_audit(tmp_path, monkeypatch, trials, protocol_result, run_id="run_t"):
    """Exercise the REAL rpr._write_promotion_audit (no reimplementation) and return
    the parsed promotion_audit.yaml it writes."""
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")
    _seed_state(tmp_path / "campaign_state.yaml", trials)
    run_dir = tmp_path / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")
    (run_dir / "artifacts" / "protocol_result.yaml").write_text(yaml.safe_dump(protocol_result), encoding="utf-8")
    rpr._write_promotion_audit(run_dir, run_id)
    return yaml.safe_load((run_dir / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8"))


# Two distinct Sharpe values -> non-degenerate variance -> happy DSR path.
_HAPPY_TRIALS = [
    {"trial_id": "a", "forecast_hash": "h1", "statistic_valid": "sharpe", "sharpe": 0.5},
    {"trial_id": "b", "forecast_hash": "h2", "statistic_valid": "sharpe", "sharpe": 1.5},
]
_HAPPY_PROTOCOL = {"per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.0}}}


# ---------------------------------------------------------------------------
# Golden path — both writers validate clean against the FIXED schema
# ---------------------------------------------------------------------------


def test_pipeline_happy_path_validates_clean(tmp_path, monkeypatch):
    audit = _run_pipeline_audit(tmp_path, monkeypatch, _HAPPY_TRIALS, _HAPPY_PROTOCOL)
    _validate(audit)
    # The 5 previously-undeclared fields are present in the artifact.
    assert audit["total_campaign_runs"] == 0
    assert audit["total_variants_tested"] == 2
    assert "dedup_removed" in audit["excluded_trial_counts"]
    assert "invalidated_artifact" in audit["excluded_trial_counts"]


def test_library_happy_path_validates_clean():
    audit = ds.compute_promotion_audit("H", 1.0, {"trial_sharpes": [dict(t) for t in _HAPPY_TRIALS]})
    _validate(audit)


# ---------------------------------------------------------------------------
# VALUE assertion — promotion_threshold_raw == E_max_SR, not the old 0.0 hardcode.
# Schema (number|null, no const) cannot catch a revert to 0.0; this can.
# ---------------------------------------------------------------------------


def test_pipeline_promotion_threshold_raw_is_e_max_sr(tmp_path, monkeypatch):
    audit = _run_pipeline_audit(tmp_path, monkeypatch, _HAPPY_TRIALS, _HAPPY_PROTOCOL)
    # expected_max_sharpe is the same E_max_SR, rounded to 4 dp; abs tol covers rounding.
    assert audit["promotion_threshold_raw"] == pytest.approx(audit["expected_max_sharpe"], abs=1e-4)
    # Explicit non-zero guard: reverting the fix to the hardcoded 0.0 fails here.
    assert abs(audit["promotion_threshold_raw"]) > 1e-6


# ---------------------------------------------------------------------------
# Degenerate paths — each still validates (proves dsr_error was ADDED, not dropped,
# and that no branch emits an undeclared field).
# ---------------------------------------------------------------------------


def test_pipeline_sparse_path_passes_deflated_null_validates_clean(tmp_path, monkeypatch):
    """CUL-163 (reconciles the CUL-14 residual): the pipeline sparse path writes
    passes_deflated_threshold=None (indeterminate — expectancy SE not stored). The
    holdout gate reads this with `is False` (run_phase1_research._route_holdout_evaluation),
    so None is a DELIBERATE tri-state — it falls through rather than terminal-rejecting a
    low-frequency candidate as "DSR too low". The schema now declares the field (and the
    nested expectancy_promotion.passes) ["boolean","null"], so the honest None validates
    CLEAN instead of false-positiving under WORKFLOW_ARTIFACT_VALIDATION=raise. The prior
    version of this test pinned the pre-reconciliation drift (asserted ValidationError);
    that reconciliation is this ticket."""
    trials = [{"trial_id": "e", "forecast_hash": "he", "statistic_valid": "expectancy", "sharpe": None, "n_trades": 10}]
    protocol = {"per_symbol_summary": {}, "hypothesis_verdict": {"diagnostics": {"below_floor_pct": 60.0}}}
    audit = _run_pipeline_audit(tmp_path, monkeypatch, trials, protocol)
    assert audit["is_sparse_trading"] is True
    assert audit["promotion_threshold_raw"] is None
    assert audit["passes_deflated_threshold"] is None
    assert audit["expectancy_promotion"]["passes"] is None
    # CUL-163 widened to the whole sparse audit: correction_method is the honest
    # expectancy label (not BLP), now permitted by the enum. All three former sparse
    # violations are gone, so the audit validates fully clean under raise-mode.
    assert audit["correction_method"] == "expectancy_t_stat_bonferroni"
    _validate(audit)  # must NOT raise — the sparse audit is now schema-valid


def test_pipeline_insufficient_trials_validates_clean(tmp_path, monkeypatch):
    trials = [{"trial_id": "a", "forecast_hash": "h1", "statistic_valid": "sharpe", "sharpe": 0.5}]
    audit = _run_pipeline_audit(tmp_path, monkeypatch, trials, _HAPPY_PROTOCOL)
    _validate(audit)
    assert "dsr_error" in audit
    assert audit["promotion_threshold_raw"] is None
    # CUL-163 guard-loss mitigation: loosening the schema to ["boolean","null"] removes the
    # only mechanical catch for an ACCIDENTAL non-sparse None — which the holdout gate reads
    # as fall-through TOWARD the seal (the unsafe direction). Pin the non-sparse degenerate
    # paths to False so a branch that regressed to None is caught here, not at the gate.
    assert audit["passes_deflated_threshold"] is False


def test_pipeline_zero_variance_validates_clean(tmp_path, monkeypatch):
    trials = [
        {"trial_id": "a", "forecast_hash": "h1", "statistic_valid": "sharpe", "sharpe": 1.0},
        {"trial_id": "b", "forecast_hash": "h2", "statistic_valid": "sharpe", "sharpe": 1.0},
    ]
    audit = _run_pipeline_audit(tmp_path, monkeypatch, trials, _HAPPY_PROTOCOL)
    _validate(audit)
    assert "dsr_error" in audit
    assert audit["promotion_threshold_raw"] is None
    # CUL-163 guard-loss mitigation (see test_pipeline_insufficient_trials_validates_clean).
    assert audit["passes_deflated_threshold"] is False


def test_library_sparse_path_unmeasurable_emits_null_validates_clean():
    # >=1 trial: total_hypotheses_tested==0 hits a pre-existing bonferroni_note
    # f-string bug ('N/A':.2f) unrelated to CUL-14 — out of scope here.
    # CUL-163: with no expectancy SE, t_stat is unmeasurable, so the library sparse path
    # now emits None (was False) to match the pipeline's honest indeterminate. Both the
    # top-level field and the nested expectancy_promotion.passes are None; validates clean.
    trials = [{"trial_id": "e", "statistic_valid": "expectancy", "sharpe": None}]
    audit = ds.compute_promotion_audit("H", None, {"trial_sharpes": trials})
    _validate(audit)
    assert audit["is_sparse_trading"] is True
    assert audit["passes_deflated_threshold"] is None
    assert audit["expectancy_promotion"]["passes"] is None


def test_library_sparse_path_with_se_emits_real_bool():
    """CUL-163: Option A preserves the library's real evaluation when expectancy SE IS
    available — t_stat = expectancy_bps / expectancy_se; > 2.0 -> True, else False, never
    None. Proves the None-on-unmeasurable change did not collapse the measurable case."""
    trials = [{"trial_id": "e", "statistic_valid": "expectancy", "sharpe": None}]
    passing = ds.compute_promotion_audit(
        "H", None, {"trial_sharpes": trials}, expectancy_bps=30.0, expectancy_se=10.0
    )  # t_stat = 3.0 > 2.0
    assert passing["passes_deflated_threshold"] is True
    assert passing["expectancy_promotion"]["passes"] is True
    _validate(passing)
    failing = ds.compute_promotion_audit(
        "H", None, {"trial_sharpes": trials}, expectancy_bps=10.0, expectancy_se=10.0
    )  # t_stat = 1.0 < 2.0
    assert failing["passes_deflated_threshold"] is False
    assert failing["expectancy_promotion"]["passes"] is False
    _validate(failing)


def test_library_insufficient_trials_validates_clean_with_dsr_error():
    trials = [{"trial_id": "a", "forecast_hash": "h1", "statistic_valid": "sharpe", "sharpe": 0.5}]
    audit = ds.compute_promotion_audit("H", 1.0, {"trial_sharpes": trials})
    _validate(audit)
    # Q4: the library path now carries dsr_error parity with the pipeline path.
    assert "dsr_error" in audit


def test_library_zero_variance_validates_clean_with_dsr_error():
    trials = [
        {"trial_id": "a", "forecast_hash": "h1", "statistic_valid": "sharpe", "sharpe": 1.0},
        {"trial_id": "b", "forecast_hash": "h2", "statistic_valid": "sharpe", "sharpe": 1.0},
    ]
    audit = ds.compute_promotion_audit("H", 1.0, {"trial_sharpes": trials})
    _validate(audit)
    assert "dsr_error" in audit


# ---------------------------------------------------------------------------
# Holdout-gate tri-state — locks the load-bearing reader semantic that makes
# Option A safe. _route_holdout_evaluation reads passes_deflated_threshold with
# `is False`, so None (indeterminate) must NOT terminal-reject at gate 1 while
# False must. A future refactor to `if not passes` would collapse the tri-state
# and reject sparse/indeterminate candidates in the unsafe direction (toward the
# seal). These two tests bite that mutation.
# ---------------------------------------------------------------------------


def _seed_run_for_gate(tmp_path, passes_value, run_id="gate_run"):
    """Seed a run dir the holdout gate can route: a promotion_audit carrying the
    given passes value, a tradable brief (clears gate 2b), and an empty pipeline
    state (clears the sticky-flag branch). No holdout_result -> a non-rejected run
    lands on step 3's human_pause."""
    run_dir = tmp_path / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    audit = {"hypothesis_id": run_id, "passes_deflated_threshold": passes_value}
    (run_dir / "artifacts" / "promotion_audit.yaml").write_text(yaml.safe_dump(audit), encoding="utf-8")
    (run_dir / "artifacts" / "research_brief.yaml").write_text(
        yaml.safe_dump({"research_only": False}), encoding="utf-8"
    )
    (run_dir / "pipeline_state.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")
    return run_dir


def test_holdout_gate_sparse_none_is_not_terminal_reject(tmp_path, monkeypatch):
    monkeypatch.setattr(rpr, "_DATA_POLICY_PATH", tmp_path / "nonexistent_policy.yaml")
    run_dir = _seed_run_for_gate(tmp_path, None)
    result = rpr._route_holdout_evaluation(run_dir, "gate_run")
    assert result != "completed_rejected"  # None falls through — not a DSR kill


def test_holdout_gate_false_is_terminal_reject(tmp_path, monkeypatch):
    # Positive control: proves gate 1 DOES terminal-reject a real False, which is
    # what makes the None-falls-through assertion above meaningful.
    monkeypatch.setattr(rpr, "_DATA_POLICY_PATH", tmp_path / "nonexistent_policy.yaml")
    run_dir = _seed_run_for_gate(tmp_path, False)
    result = rpr._route_holdout_evaluation(run_dir, "gate_run")
    assert result == "completed_rejected"


# ---------------------------------------------------------------------------
# CUL-163 backstop (guard-loss, correction_method): widening the enum to two values
# means a NON-sparse audit accidentally carrying the sparse "expectancy_t_stat_bonferroni"
# label would now validate against the schema. test_each_path_is_internally_consistent
# in test_correction_method_label_agrees.py counts only "bailey" labels, so a
# non-sparse site regressed to the expectancy label slips past it. Pin the label to
# is_sparse_trading BY VALUE on both writers so that regression is caught here.
# Mutation-proof: emit the expectancy label on a non-sparse site -> these fail.
# ---------------------------------------------------------------------------


def test_pipeline_correction_method_agrees_with_is_sparse(tmp_path, monkeypatch):
    sparse = _run_pipeline_audit(
        tmp_path,
        monkeypatch,
        [{"trial_id": "e", "forecast_hash": "he", "statistic_valid": "expectancy", "sharpe": None, "n_trades": 10}],
        {"per_symbol_summary": {}, "hypothesis_verdict": {"diagnostics": {"below_floor_pct": 60.0}}},
        run_id="sp",
    )
    assert sparse["is_sparse_trading"] is True
    assert sparse["correction_method"] == "expectancy_t_stat_bonferroni"
    nonsparse = _run_pipeline_audit(tmp_path, monkeypatch, _HAPPY_TRIALS, _HAPPY_PROTOCOL, run_id="ns")
    assert nonsparse["is_sparse_trading"] is False
    assert nonsparse["correction_method"] == "bailey_lopezdeprado_2014"


def test_library_correction_method_agrees_with_is_sparse():
    sparse = ds.compute_promotion_audit(
        "H", None, {"trial_sharpes": [{"trial_id": "e", "statistic_valid": "expectancy", "sharpe": None}]}
    )
    assert sparse["is_sparse_trading"] is True
    assert sparse["correction_method"] == "expectancy_t_stat_bonferroni"
    nonsparse = ds.compute_promotion_audit("H", 1.0, {"trial_sharpes": [dict(t) for t in _HAPPY_TRIALS]})
    assert nonsparse["is_sparse_trading"] is False
    assert nonsparse["correction_method"] == "bailey_lopezdeprado_2014"
