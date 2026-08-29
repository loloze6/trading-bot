"""
Known-answer tests for run_artifact.py::build_bar_equity's degenerate-input
handling and regime-label normalization (2026-07-31 fix round,
fix/metrics-bar-equity).

The bar_equity flag is an explicit opt-in, so degenerate input must raise
ValueError, never silently return an empty/misleading block -- see
build_bar_equity's own docstring for the exact list of conditions.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from reporting.run_artifact import build_bar_equity

_REQUIRED_COLS = [
    "regime",
    "timestamp",
    "postRebalance_total_value",
    "postRebalance_current_allocation",
    "previous_allocation",
]


def _bars(regimes, values=None, timestamps=None, alloc=None, prev_alloc=None):
    n = len(regimes)
    values = values if values is not None else [1000.0 + i for i in range(n)]
    timestamps = timestamps if timestamps is not None else pd.date_range("2024-01-01", periods=n, freq="h")
    alloc = alloc if alloc is not None else [0.0] * n
    prev_alloc = prev_alloc if prev_alloc is not None else [0.0] * n
    return pd.DataFrame(
        {
            "regime": regimes,
            "timestamp": timestamps,
            "postRebalance_total_value": values,
            "postRebalance_current_allocation": alloc,
            "previous_allocation": prev_alloc,
        }
    )


def test_missing_required_column_raises():
    df = _bars(["unknown"] * 5).drop(columns=["previous_allocation"])
    with pytest.raises(ValueError, match="missing required columns"):
        build_bar_equity(df)


def test_zero_ready_rows_raises():
    df = _bars(["NOT_READY"] * 5)
    with pytest.raises(ValueError, match="zero bars remain"):
        build_bar_equity(df)


def test_nan_in_required_column_among_ready_rows_raises():
    df = _bars(["NOT_READY", "unknown", "unknown", "unknown"])
    df.loc[df.index[-1], "postRebalance_total_value"] = np.nan
    with pytest.raises(ValueError, match="NaN found"):
        build_bar_equity(df)


def test_nonfinite_max_drawdown_raises():
    """All-zero equity -> running max is 0 throughout -> 0/0 -> NaN drawdown."""
    df = _bars(["NOT_READY", "unknown", "unknown", "unknown"], values=[1000.0, 0.0, 0.0, 0.0])
    with pytest.raises(ValueError, match="non-finite"):
        build_bar_equity(df)


def test_regime_normalization_strips_whitespace_and_case():
    """' not_ready ', 'Not_Ready', 'NOT_READY ' etc. must all be excluded as
    warmup, not just the exact literal string."""
    df = _bars([" not_ready ", "Not_Ready", "NOT_READY", "unknown", "unknown"])
    result = build_bar_equity(df)
    assert result["n_bars_warmup_excluded"] == 3
    assert result["n_bars_total"] == 5


def test_n_bars_warmup_excluded_zero_is_legal_not_an_error():
    """A warmup_prefetch-style run can be ready from bar 0 -- zero excluded
    bars must NOT raise, and must be reported honestly via the field."""
    df = _bars(["unknown", "unknown", "trending", "chop"])
    result = build_bar_equity(df)
    assert result["n_bars_warmup_excluded"] == 0
    assert result["n_bars_total"] == 4


def test_result_includes_n_daily_returns_and_n_downside_days():
    """A guarded 0.0 sharpe/sortino must be distinguishable from a genuinely
    computed 0.0 by checking these counts."""
    df = _bars(["unknown"] * 4)  # 4 bars, all same hour-spaced timestamps -> 1 day -> 0 returns
    result = build_bar_equity(df)
    assert "n_daily_returns" in result
    assert "n_downside_days" in result
    assert result["n_daily_returns"] == 0  # all 4 bars land on the same calendar day
