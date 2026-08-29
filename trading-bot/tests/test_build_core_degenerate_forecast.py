"""
Known-answer test for run_artifact.py::build_core's forecast_return_corr
(2026-07-09 fix). Reproduces the exact P4_ts_trend degenerate shape (a
long-only signal whose active-bar forecast is a single constant magnitude)
directly against build_core, proving it now reports None/None instead of the
old hardcoded corr=0.0, p=1.0.
"""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from reporting.run_artifact import build_core


def _bars(forecasts, closes):
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2020-01-01", periods=len(forecasts), freq="D"),
            "forecast": forecasts,
            "close": closes,
        }
    )


def test_long_only_constant_forecast_gives_none_not_zero():
    """
    Long-only signal: forecast is either 0.0 (flat) or exactly +10.0 (active),
    never varying, never negative -- the exact SmaTrendLongOnlyComponent shape.
    Active-bar forecast has zero variance -- correlation must be None, not the
    old hardcoded 0.0/p=1.0.
    """
    forecasts = [10.0, 10.0, 0.0, 0.0, 10.0, 10.0, 10.0, 0.0, 10.0, 0.0] * 3
    closes = [100 + i * 0.3 + (1 if f else -1) for i, f in enumerate(forecasts)]

    core = build_core(
        metrics_dict={}, completed_trades=[], bars_df=_bars(forecasts, closes)
    )

    assert core["forecast_return_corr"] is None, (
        f"expected None (undefined) for a constant-when-active signal, got "
        f"{core['forecast_return_corr']!r} -- the old bug hardcoded this to 0.0"
    )
    assert core["forecast_return_corr_pvalue"] is None, (
        f"expected None -- a p-value must never be derived from an undefined "
        f"correlation, got {core['forecast_return_corr_pvalue']!r} "
        f"(the old bug fabricated p=1.0 here)"
    )


def test_two_sided_varying_forecast_gives_a_real_value():
    """Sanity check: a signal with real magnitude variation among active bars
    (e.g. MACD-style ±10 events, or here a smoothly varying forecast) must
    still produce a real, defined correlation -- the fix must not make EVERY
    forecast_return_corr silently None."""
    n = 40
    forecasts = [
        ((-1) ** i) * (5 + i % 5) for i in range(n)
    ]  # varies in magnitude and sign
    closes = [100 + sum(forecasts[: i + 1]) * 0.01 for i in range(n)]

    core = build_core(
        metrics_dict={}, completed_trades=[], bars_df=_bars(forecasts, closes)
    )

    assert core["forecast_return_corr"] is not None
