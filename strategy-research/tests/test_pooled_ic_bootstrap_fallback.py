"""
Known-answer tests for run_protocol.py's block-bootstrap IC fallback
(2026-07-09, P4_ts_trend). evaluate_against_decision_rules's "Walk-forward
pooled IC" criterion was ALWAYS UNTESTED (no keyword resolved it at all) --
extending it surfaced a real collision bug during development: a naive broad
keyword also matched a DIFFERENT criterion about p-value significance, letting
a real IC value coincidentally satisfy an unrelated p<0.05 threshold and flip
a verdict to a false PROMOTE. These tests lock in both the fallback's
correctness and the collision fix.
"""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

TOOLS_PATH = Path(__file__).parent.parent / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import run_protocol as rp


def _write_bars(run_dir: Path, forecasts, closes):
    run_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({
        "timestamp": pd.date_range("2020-01-01", periods=len(forecasts), freq="D"),
        "forecast": forecasts,
        "close": closes,
    })
    df.to_csv(run_dir / "bars.csv", index=False)


def test_resolve_field_significance_wording_never_maps_to_ic(monkeypatch=None):
    """The collision bug: a p-value criterion must never resolve to
    median_forecast_return_corr, no matter how the sentence mentions 'ic'."""
    text = "Per-era IC decomposition: block-bootstrapped pooled_ic is statistically significant (p<0.05)"
    assert rp._resolve_field(text) is None


def test_resolve_field_magnitude_wording_maps_to_ic():
    text = "Walk-forward pooled IC (Spearman, all bars ungated) >= 1.5-2.0% across 12 overlapping 30-day windows"
    assert rp._resolve_field(text) == "median_forecast_return_corr"


def test_impossible_ic_threshold_returns_spec_error_not_fail():
    """2026-07-09 incident: 'IC >= 1.5%' parses to threshold=1.5, impossible for
    a correlation coefficient (|corr|<=1 always). Must report SPEC_ERROR, not
    silently evaluate as FAIL (which would look like real evidence)."""
    text = "Walk-forward pooled IC (Spearman, all bars ungated) >= 1.5-2.0% across 12 overlapping 30-day windows"
    extended = {"BTCUSDT": {"median_forecast_return_corr": 0.037}}
    row = rp._evaluate_criterion(text, extended, is_reject=False)
    assert row["result"] == "SPEC_ERROR"


def test_spec_error_does_not_count_as_evaluated_for_promote(tmp_path):
    """A SPEC_ERROR criterion must not let a hypothesis reach 'promote' just
    because it technically isn't a FAIL."""
    per_symbol_summary = {"BTCUSDT": {"median_sharpe": 1.0, "max_abs_drawdown_pct": 5.0, "min_trade_count": 5}}
    results = [
        {"symbol": "BTCUSDT", "window": "2020-01", "run_id": "r1",
         "core": {"win_rate": 60.0, "forecast_return_corr": 0.03, "gross_pnl": 10.0,
                   "cost_drag_pct": 1.0, "avg_trade_duration_bars": 5.0, "trade_count": 5}},
    ]
    vp = {
        "decision_rules": {
            "approve_if_all_met": [
                "Walk-forward pooled IC (Spearman, all bars ungated) >= 1.5-2.0%",
            ],
            "reject_if_any_met": [],
        },
    }
    hv = rp.evaluate_against_decision_rules(per_symbol_summary, results, vp, None, runs_root=None)
    assert hv["verdict"] != "promote"


def test_non_degenerate_uses_plain_median_not_bootstrap():
    rows = [
        {"symbol": "BTCUSDT", "window": "2020-01", "run_id": "r1",
         "core": {"forecast_return_corr": 0.05}},
        {"symbol": "BTCUSDT", "window": "2020-02", "run_id": "r2",
         "core": {"forecast_return_corr": 0.07}},
    ]
    corr, method = rp._pooled_ic_with_bootstrap_fallback(rows, runs_root=None)
    assert method == "per_window_median_pearson"
    assert corr == 0.06


def test_degenerate_falls_back_to_bootstrap(tmp_path):
    """All windows report forecast_return_corr=None (the long-only constant-
    magnitude shape) -- must fall back to the block-bootstrap on pooled bars.csv
    data, not stay None forever."""
    runs_root = tmp_path / "results"

    # Two windows, deterministic positive relationship: active (10.0) precedes
    # a positive return, inactive (0.0) precedes a negative one.
    _write_bars(
        runs_root / "run_w1",
        forecasts=[10.0, 10.0, 0.0, 0.0] * 10,
        closes=[100 + i * (0.3 if (i // 2) % 2 == 0 else -0.3) for i in range(40)],
    )
    _write_bars(
        runs_root / "run_w2",
        forecasts=[10.0, 10.0, 0.0, 0.0] * 10,
        closes=[100 + i * (0.3 if (i // 2) % 2 == 0 else -0.3) for i in range(40)],
    )

    rows = [
        {"symbol": "BTCUSDT", "window": "2020-01", "run_id": "run_w1",
         "core": {"forecast_return_corr": None}},
        {"symbol": "BTCUSDT", "window": "2020-02", "run_id": "run_w2",
         "core": {"forecast_return_corr": None}},
    ]
    corr, method = rp._pooled_ic_with_bootstrap_fallback(rows, runs_root=str(runs_root))
    assert method == "block_bootstrap_all_bars_v1"
    assert corr is not None


def test_degenerate_no_bars_csv_returns_none():
    rows = [
        {"symbol": "BTCUSDT", "window": "2020-01", "run_id": "missing",
         "core": {"forecast_return_corr": None}},
    ]
    corr, method = rp._pooled_ic_with_bootstrap_fallback(rows, runs_root="/nonexistent/path")
    assert corr is None
    assert method is None


def test_build_extended_summary_populates_ic_fields(tmp_path):
    runs_root = tmp_path / "results"
    _write_bars(
        runs_root / "run_a",
        forecasts=[10.0] * 20 + [0.0] * 20,
        closes=[100 + i * 0.1 for i in range(40)],
    )
    per_symbol_summary = {"BTCUSDT": {"median_sharpe": -1.0}}
    results = [
        {"symbol": "BTCUSDT", "window": "2020-01", "run_id": "run_a",
         "core": {"win_rate": 40.0, "forecast_return_corr": None}},
    ]
    extended = rp._build_extended_summary(per_symbol_summary, results, str(runs_root))
    assert "median_forecast_return_corr" in extended["BTCUSDT"]
    assert "median_forecast_return_corr_method" in extended["BTCUSDT"]
