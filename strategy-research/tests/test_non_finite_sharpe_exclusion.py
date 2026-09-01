"""CUL-31: a NaN/inf sharpe (a contract-legitimate merged row — e.g. a killed-run
placeholder from union_merge_trial_ledgers) must be excluded from the Sharpe pool
with a visible counter, on BOTH the library path (deflate_sharpe.load_sharpe_trials)
and the pipeline path (run_phase1_research._write_promotion_audit).

Left unguarded, a single non-finite value makes mu_sr/sigma_sr/dsr all NaN — and the
`sigma_sr < 1e-10` degenerate-variance guard does NOT catch it (NaN < 1e-10 is False),
so a silently-corrupted DSR is written with no error flag.

N-honesty (red-team M1): excluding a non-finite sharpe must NOT shrink the DSR trial
count (n_dsr_total / total_hypotheses_tested) — the multiple-testing N counts every
recorded attempt; only the real-Sharpe-value sample (n_trials_used) drops.
"""

import math
import sys
from pathlib import Path

import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(WORKFLOW_PATH))

import deflate_sharpe as ds  # noqa: E402
import run_phase1_research as rpr  # noqa: E402


def _run_pipeline_audit(tmp_path, monkeypatch, trials, run_id="run_nf"):
    """Exercise the REAL rpr._write_promotion_audit (the pipeline :5218 twin, no
    reimplementation) and return the parsed promotion_audit.yaml."""
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")
    (tmp_path / "campaign_state.yaml").write_text(
        yaml.safe_dump({"trial_sharpes": [dict(t) for t in trials]}), encoding="utf-8"
    )
    run_dir = tmp_path / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(yaml.safe_dump({}), encoding="utf-8")
    (run_dir / "artifacts" / "protocol_result.yaml").write_text(
        yaml.safe_dump({"per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.0}}}), encoding="utf-8"
    )
    rpr._write_promotion_audit(run_dir, run_id)
    return yaml.safe_load((run_dir / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8"))


# NaN + inf + two finite Sharpes.
_MIXED = [
    {"trial_id": "a", "forecast_hash": "h1", "statistic_valid": "sharpe", "sharpe": float("nan")},
    {"trial_id": "b", "forecast_hash": "h2", "statistic_valid": "sharpe", "sharpe": float("inf")},
    {"trial_id": "c", "forecast_hash": "h3", "statistic_valid": "sharpe", "sharpe": 0.5},
    {"trial_id": "d", "forecast_hash": "h4", "statistic_valid": "sharpe", "sharpe": 1.5},
]


# ---------------------------------------------------------------------------
# Library path (deflate_sharpe.load_sharpe_trials / compute_promotion_audit)
# ---------------------------------------------------------------------------


def test_library_load_sharpe_trials_filters_and_counts_non_finite():
    sharpe_values, excluded = ds.load_sharpe_trials({"trial_sharpes": [dict(t) for t in _MIXED]})
    assert sharpe_values == [0.5, 1.5]
    assert excluded["non_finite_sharpe"] == 2
    assert excluded["no_sharpe_value"] == 0


def test_library_compute_promotion_audit_dsr_finite_and_n_honest():
    audit = ds.compute_promotion_audit("H", 1.0, {"trial_sharpes": [dict(t) for t in _MIXED]})
    dsr = audit["deflated_sharpe_ratio"]
    assert dsr is not None and math.isfinite(dsr)
    assert audit["excluded_trial_counts"]["non_finite_sharpe"] == 2
    # N-honesty: N counts all 4 deduped trials; only the finite sample (2) drops out.
    assert audit["total_hypotheses_tested"] == 4
    assert audit["n_trials_used"] == 2


# ---------------------------------------------------------------------------
# Pipeline path (run_phase1_research._write_promotion_audit — the :5218 twin)
# ---------------------------------------------------------------------------


def test_pipeline_filters_and_counts_non_finite(tmp_path, monkeypatch):
    audit = _run_pipeline_audit(tmp_path, monkeypatch, _MIXED)
    assert audit["excluded_trial_counts"]["non_finite_sharpe"] == 2
    dsr = audit["deflated_sharpe_ratio"]
    assert dsr is not None and math.isfinite(dsr)
    # N-honesty pinned on the executed path too.
    assert audit["total_hypotheses_tested"] == 4
    assert audit["n_trials_used"] == 2


def test_pipeline_single_nan_does_not_corrupt_dsr(tmp_path, monkeypatch):
    """The precise failure mode: one NaN among enough finite trials. Unguarded, the
    zero-variance guard misses it (NaN < 1e-10 is False) and dsr comes out NaN."""
    trials = [
        {"trial_id": "a", "forecast_hash": "h1", "statistic_valid": "sharpe", "sharpe": float("nan")},
        {"trial_id": "b", "forecast_hash": "h2", "statistic_valid": "sharpe", "sharpe": 0.5},
        {"trial_id": "c", "forecast_hash": "h3", "statistic_valid": "sharpe", "sharpe": 1.5},
    ]
    audit = _run_pipeline_audit(tmp_path, monkeypatch, trials)
    assert audit["excluded_trial_counts"]["non_finite_sharpe"] == 1
    assert math.isfinite(audit["deflated_sharpe_ratio"])
    assert audit["total_hypotheses_tested"] == 3  # NaN row still counted in N
    assert audit["n_trials_used"] == 2
