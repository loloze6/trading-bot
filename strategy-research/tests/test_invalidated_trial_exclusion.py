"""
F8b (2026-07-04) regression test.

Both promotion-audit code paths — tools/deflate_sharpe.py (standalone holdout tool)
and workflow/run_phase1_research.py::_write_promotion_audit (inline promote-verdict
path) — independently loop over campaign_state.trial_sharpes and previously counted
EVERY trial toward total_hypotheses_tested (the multiple-testing correction basis),
with no check for invalidated_artifact. run_044's real trial_sharpes entry
(FundingRateMeanReversionComponent's threshold=0 divide-by-zero, F5a — the hypothesis
was never actually tested) is the fixture: it must be excluded from both.
"""
import sys
from pathlib import Path

import pytest
import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(WORKFLOW_PATH))

import deflate_sharpe as ds
import run_phase1_research as rpr

# run_044's REAL invalidated trial_sharpes entry, frozen verbatim (see
# campaign_state.yaml trial_sharpes run_044 for the live version).
_RUN_044_INVALIDATED_TRIAL = {
    "trial_id": "run_044",
    "source": "prescreen",
    "route": "kill_no_ic",
    "sharpe": None,
    "expectancy_bps": None,
    "n_trades": 0,
    "statistic_valid": "neither",
    "ic_pooled": None,
    "cost_pass": False,
    "invalidated_artifact": True,
    "invalidation_reason": "F5 (2026-07-04): active_n_bars=0 was a divide-by-zero artifact.",
}

_RUN_044_POST_F5_VALID_TRIAL = {
    "trial_id": "run_044_post_f5",
    "hypothesis_id": "FUNDING_RATE_CONTINUOUS_MEAN_REVERSION",
    "source": "prescreen",
    "route": "kill_no_ic",
    "sharpe": None,
    "expectancy_bps": None,
    "n_trades": 0,
    "statistic_valid": "neither",
    "ic_pooled": 0.016737,
    "cost_pass": False,
    "forecast_hash": "e3b50e8d434608ed",
}

_GENUINE_SHARPE_TRIALS = [
    {"trial_id": "run_010", "sharpe": 0.3, "statistic_valid": "sharpe", "forecast_hash": "aaa"},
    {"trial_id": "run_011", "sharpe": -0.1, "statistic_valid": "sharpe", "forecast_hash": "bbb"},
    {"trial_id": "run_012", "sharpe": 0.15, "statistic_valid": "sharpe", "forecast_hash": "ccc"},
]


# ---------------------------------------------------------------------------
# tools/deflate_sharpe.py
# ---------------------------------------------------------------------------

def test_exclude_invalidated_trials_removes_run_044():
    records = _GENUINE_SHARPE_TRIALS + [_RUN_044_INVALIDATED_TRIAL, _RUN_044_POST_F5_VALID_TRIAL]
    kept, n_excluded = ds.exclude_invalidated_trials(records)
    assert n_excluded == 1
    assert all(not r.get("invalidated_artifact") for r in kept)
    assert _RUN_044_POST_F5_VALID_TRIAL in kept  # the REAL post-fix trial must survive


def test_promotion_audit_total_hypotheses_tested_excludes_invalidated():
    campaign_state = {"trial_sharpes": _GENUINE_SHARPE_TRIALS + [_RUN_044_INVALIDATED_TRIAL]}
    audit = ds.compute_promotion_audit(
        hypothesis_id="TEST", candidate_sr=0.4, campaign_state=campaign_state,
    )
    assert audit["total_hypotheses_tested"] == 3, (
        f"expected 3 (invalidated trial excluded), got {audit['total_hypotheses_tested']}"
    )
    assert audit["excluded_trial_counts"]["invalidated_artifact"] == 1


def test_promotion_audit_dsr_unaffected_by_invalidated_trial_with_no_sharpe():
    """Since run_044's invalidated trial has sharpe=None anyway, DSR itself doesn't
    change numerically -- but total_hypotheses_tested (the correction basis) must."""
    with_invalidated = ds.compute_promotion_audit(
        "TEST", 0.4, {"trial_sharpes": _GENUINE_SHARPE_TRIALS + [_RUN_044_INVALIDATED_TRIAL]}
    )
    without_invalidated = ds.compute_promotion_audit(
        "TEST", 0.4, {"trial_sharpes": _GENUINE_SHARPE_TRIALS}
    )
    assert with_invalidated["deflated_sharpe_ratio"] == without_invalidated["deflated_sharpe_ratio"]
    assert with_invalidated["total_hypotheses_tested"] == without_invalidated["total_hypotheses_tested"]


# ---------------------------------------------------------------------------
# workflow/run_phase1_research.py::_write_promotion_audit (independent implementation)
# ---------------------------------------------------------------------------

def test_write_promotion_audit_excludes_invalidated_trial(tmp_path, monkeypatch):
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")
    (tmp_path / "campaign_state.yaml").write_text(yaml.safe_dump({
        "trial_sharpes": _GENUINE_SHARPE_TRIALS + [_RUN_044_INVALIDATED_TRIAL],
        "runs": [],
    }), encoding="utf-8")

    run_dir = tmp_path / "runs" / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "TEST"}), encoding="utf-8"
    )
    (run_dir / "artifacts" / "protocol_result.yaml").write_text(yaml.safe_dump({
        "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 0.4}},
        "hypothesis_verdict": {"diagnostics": {"below_floor_pct": 0.0}},
    }), encoding="utf-8")

    rpr._write_promotion_audit(run_dir, "run_test")

    audit = yaml.safe_load((run_dir / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8"))
    assert audit["total_variants_tested"] == 3, (
        f"expected 3 (invalidated trial excluded from _write_promotion_audit's own "
        f"independent count), got {audit['total_variants_tested']}"
    )
    # COUNT-DIV fix (2026-08-17): "total_hypotheses_tested" now matches
    # promotion_audit.schema.json's declared meaning (deduplicated trial_sharpes
    # count) instead of the unrelated len(campaign.runs) it held before. No dedup
    # collisions in this fixture, so it equals total_variants_tested here (3).
    assert audit["total_hypotheses_tested"] == 3
    # The displaced len(campaign.runs) metric survives under its own honest name.
    assert audit["total_campaign_runs"] == 0
    assert audit["excluded_trial_counts"]["invalidated_artifact"] == 1


def test_write_promotion_audit_h1_uses_honest_n_not_just_sharpe_count(tmp_path, monkeypatch):
    """H1 fix (2026-08-16, issue #28), mirrored-path proof. 10 prescreen kills + 1
    real sharpe trial: pre-fix, N (n_trials, the real-Sharpe-value count) was 1, hit
    the N<2 branch, dsr_error said "Insufficient sharpe-valid trials for DSR (n=1,
    need >=2)". Post-fix, n_dsr_total (len(deduped_trials) == 11) clears that gate,
    and the DIFFERENT, honest refusal fires instead -- naming N=11 explicitly. Same
    shape as deflate_sharpe.py's test_h1_promotion_audit_wires_full_n_into_dsr, for
    the independent inline implementation."""
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")
    kills = [
        {"trial_id": f"run_k{i}", "source": "prescreen", "route": "kill_no_ic",
         "sharpe": None, "statistic_valid": "neither", "forecast_hash": f"kill{i}"}
        for i in range(10)
    ]
    one_real = [{"trial_id": "run_real", "sharpe": 0.42, "statistic_valid": "sharpe",
                 "forecast_hash": "real1"}]
    (tmp_path / "campaign_state.yaml").write_text(yaml.safe_dump({
        "trial_sharpes": kills + one_real, "runs": [],
    }), encoding="utf-8")

    run_dir = tmp_path / "runs" / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "TEST"}), encoding="utf-8")
    (run_dir / "artifacts" / "protocol_result.yaml").write_text(yaml.safe_dump({
        "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 0.5}},
        "hypothesis_verdict": {"diagnostics": {"below_floor_pct": 0.0}},
    }), encoding="utf-8")

    rpr._write_promotion_audit(run_dir, "run_test")
    audit = yaml.safe_load((run_dir / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8"))

    assert audit["total_variants_tested"] == 11  # all 11 real attempts, kills included.
    # COUNT-DIV fix (2026-08-17): now matches total_variants_tested (no dedup
    # collisions in this fixture) instead of the old len(campaign.runs)=0 bug.
    assert audit["total_hypotheses_tested"] == 11
    assert audit["total_campaign_runs"] == 0
    assert audit["n_trials_used"] == 1  # still only 1 real Sharpe value -- a separate question.
    assert audit["deflated_sharpe_ratio"] is None  # correctly still None -- can't estimate variance from 1 point.
    assert audit["dsr_error"] == (
        "N=11 trials recorded (multiple-testing count is honest), but only 1 produced "
        "a real Sharpe value -- need >= 2 real Sharpe values to estimate the trial "
        "distribution's variance. A large N does not fix an unmeasurable variance."
    ), audit["dsr_error"]
