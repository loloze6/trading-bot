"""CUL-218 follow-up (code review, 2026-09-03): panel_backtester.sma_long_only_signal
had no test pinning its actual computed output -- the only file that imports it,
test_panel_backtester_window_gate.py, monkeypatches it away entirely (by design, to
avoid an SMA-100 warmup confound; see that file's docstring). That left the CUL-218
fillna->shift(fill_value=False) change unpinned: nothing would catch a future pandas
version silently changing shift/fillna semantics, or a regression in this file's own
edits to the function.
"""

import os
import sys

import numpy as np
import pandas as pd
import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.join(os.path.dirname(_HERE), "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import panel_backtester as pb  # noqa: E402


def test_sma_long_only_signal_matches_an_independent_recomputation():
    """Independent oracle: recompute SMA_L, shift, and the > comparison here
    from scratch (not by calling any panel_backtester helper), then compare
    bar-for-bar against the function under test."""
    idx = pd.date_range("2018-01-01", periods=250, freq="D")
    rng = np.random.RandomState(20260903)
    closes = pd.Series(100.0 + rng.normal(0, 1, len(idx)).cumsum(), index=idx)

    L = 20
    expected_sma = closes.rolling(L).mean()
    expected = (closes > expected_sma).shift(1)
    expected = expected.where(expected.notna(), False).astype(bool)

    got = pb.sma_long_only_signal(closes, L=L)

    assert got.dtype == bool
    pd.testing.assert_series_equal(got, expected, check_names=False)


def test_sma_long_only_signal_first_bar_is_always_false():
    """Bar 0 has no T-1 to compare -- the shift-introduced fill must be False
    (flat), never True (a phantom long position with no basis)."""
    idx = pd.date_range("2018-01-01", periods=5, freq="D")
    closes = pd.Series([100.0, 200.0, 300.0, 400.0, 500.0], index=idx)
    got = pb.sma_long_only_signal(closes, L=2)
    assert bool(got.iloc[0]) is False


def test_sma_long_only_signal_flips_true_exactly_when_prior_close_crosses_above_sma():
    """Hand-computed crossover: a flat run below a rising ramp keeps the
    signal False, then a single spike takes close above the (still-lagging)
    SMA on that bar, making the NEXT bar's signal True (T-1 comparison)."""
    idx = pd.date_range("2018-01-01", periods=6, freq="D")
    closes = pd.Series([100.0, 100.0, 100.0, 100.0, 200.0, 100.0], index=idx)
    got = pb.sma_long_only_signal(closes, L=3)
    # index 4: close=200 > SMA_3([100,100,100])=100 -> True, but signal is
    # SHIFTED, so this becomes visible at index 5, not index 4.
    assert list(got) == [False, False, False, False, False, True]


def test_sma_long_only_signal_output_is_bool_dtype_not_object():
    """CUL-218 regression guard: shift(fill_value=False) must not leave the
    series as object dtype the way shift().fillna(False) risked under some
    pandas versions -- downstream boolean indexing (simulate_long_flat)
    requires a real bool dtype."""
    idx = pd.date_range("2018-01-01", periods=10, freq="D")
    closes = pd.Series(np.linspace(100, 110, 10), index=idx)
    got = pb.sma_long_only_signal(closes, L=3)
    assert got.dtype == bool
