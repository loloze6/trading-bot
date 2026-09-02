"""
CUL-204 follow-up: panel_backtester._window_gate builds its score-window clip
via pd.Timedelta(days=1)/pd.Timedelta(days=2) on bare ints, which emits the
numpy generic-unit DeprecationWarning at construction (fixed to
datetime.timedelta, matching the backlog-3c precedent commit 674e49e7). No
dedicated test file existed for panel_backtester.py before this fix; this one
covers the touched lines only, with a synthetic (never real-cache) fixture.
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd
import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.join(os.path.dirname(_HERE), "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import panel_backtester as pb  # noqa: E402


def _synthetic_daily_ohlcv(n=300, start="2018-01-01", seed=20260902):
    idx = pd.date_range(start, periods=n, freq="D")
    rng = np.random.RandomState(seed)
    noise = rng.normal(0, 1, n).cumsum()
    close = np.abs(100.0 + noise) + 1.0
    return pd.DataFrame(
        {
            "timestamp": idx,
            "open": close,
            "high": close * 1.001,
            "low": close * 0.999,
            "close": close,
            "volume": 1000.0,
        }
    )


def test_window_gate_raises_no_deprecation_warning():
    df = _synthetic_daily_ohlcv()
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        result = pb._window_gate(df, "2018-04-01", "2018-10-01")
    assert "trade_count" in result


def test_window_gate_score_window_is_start_plus_1d_end_minus_2d(monkeypatch):
    """Pins the exact clip so a +-1-day shift of EITHER boundary changes the
    scored trade's entry or exit price -- refuted in an earlier draft of this
    test (round-2 blind review): that version independently recomputed the
    same +1D/-2D mask and reran the REAL sma_long_only_signal(L=100) against
    it, but with only ~90 days of history before the window the signal has
    not exited SMA-100 warmup yet, so it stays constant (flat) all the way to
    2018-04-12 -- shifting the start boundary by up to +10 days landed on the
    same constant signal value and left trade_count/net_return unchanged.
    Insensitive to the very thing it claimed to pin.

    Fixed by removing the dependency on SMA-100 warmup entirely: the signal
    is monkeypatched to constant-True across the whole fixture, so
    simulate_long_flat enters at the FIRST masked bar (no signal transition)
    and force-closes at the LAST masked bar -- i.e. entry/exit land exactly
    on the start+1d / end-2d boundary dates. Closes are a strictly increasing
    linear series (100 + day-index), so entry/exit prices -- and therefore
    net_return_pct -- are unique per calendar day and change under either
    mutation below."""
    idx = pd.date_range("2018-01-01", periods=400, freq="D")
    close = 100.0 + np.arange(len(idx), dtype=float)
    df = pd.DataFrame({
        "timestamp": idx, "open": close, "high": close + 0.5,
        "low": close - 0.5, "close": close, "volume": 1000.0,
    })
    monkeypatch.setattr(pb, "sma_long_only_signal", lambda closes, L=100: pd.Series(True, index=closes.index))

    entry_day = (pd.Timestamp("2018-04-01") + pd.Timedelta(1, unit="D") - idx[0]).days
    exit_day = (pd.Timestamp("2018-10-01") - pd.Timedelta(2, unit="D") - idx[0]).days
    Pe, Px = float(close[entry_day]), float(close[exit_day])
    rate = pb.DEFAULT_COMMISSION_RATE
    expected_net_return_pct = round(((1 - rate) * (Px / Pe) - 1) * 100, 3)

    result = pb._window_gate(df, "2018-04-01", "2018-10-01")
    assert result["trade_count"] == 1
    assert result["net_return_pct"] == pytest.approx(expected_net_return_pct, abs=1e-6)
