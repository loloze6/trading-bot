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


def test_pipeline_sparse_path_residual_drift_is_passes_deflated_null(tmp_path, monkeypatch):
    """RESIDUAL (out of CUL-14 scope, surfaced by this validation work): the pipeline
    sparse path writes passes_deflated_threshold=None (indeterminate — expectancy SE
    not yet stored), which violates the schema's boolean type. The library sparse path
    emits False for the same case, so this is also a pipeline-vs-library lockstep drift.
    CUL-14's field-audit enumerated 5 undeclared fields + the promotion_threshold_raw
    hardcode; passes_deflated_threshold nullability was NOT among them and reconciling
    the two sparse paths (or making the field nullable) is a separate semantic decision.
    Commit 3's warn-mode is exactly what surfaces this class of residual without halting
    runs. This test pins the residual so a future reconciliation flips it deliberately."""
    trials = [{"trial_id": "e", "forecast_hash": "he", "statistic_valid": "expectancy", "sharpe": None, "n_trades": 10}]
    protocol = {"per_symbol_summary": {}, "hypothesis_verdict": {"diagnostics": {"below_floor_pct": 60.0}}}
    audit = _run_pipeline_audit(tmp_path, monkeypatch, trials, protocol)
    assert audit["is_sparse_trading"] is True
    assert audit["promotion_threshold_raw"] is None
    assert audit["passes_deflated_threshold"] is None  # the residual
    with pytest.raises(jsonschema.ValidationError) as exc:
        _validate(audit)
    assert "passes_deflated_threshold" in str(exc.value)


def test_pipeline_insufficient_trials_validates_clean(tmp_path, monkeypatch):
    trials = [{"trial_id": "a", "forecast_hash": "h1", "statistic_valid": "sharpe", "sharpe": 0.5}]
    audit = _run_pipeline_audit(tmp_path, monkeypatch, trials, _HAPPY_PROTOCOL)
    _validate(audit)
    assert "dsr_error" in audit
    assert audit["promotion_threshold_raw"] is None


def test_pipeline_zero_variance_validates_clean(tmp_path, monkeypatch):
    trials = [
        {"trial_id": "a", "forecast_hash": "h1", "statistic_valid": "sharpe", "sharpe": 1.0},
        {"trial_id": "b", "forecast_hash": "h2", "statistic_valid": "sharpe", "sharpe": 1.0},
    ]
    audit = _run_pipeline_audit(tmp_path, monkeypatch, trials, _HAPPY_PROTOCOL)
    _validate(audit)
    assert "dsr_error" in audit
    assert audit["promotion_threshold_raw"] is None


def test_library_sparse_path_validates_clean():
    # >=1 trial: total_hypotheses_tested==0 hits a pre-existing bonferroni_note
    # f-string bug ('N/A':.2f) unrelated to CUL-14 — out of scope here.
    trials = [{"trial_id": "e", "statistic_valid": "expectancy", "sharpe": None}]
    audit = ds.compute_promotion_audit("H", None, {"trial_sharpes": trials})
    _validate(audit)
    assert audit["is_sparse_trading"] is True


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
