"""
Known-answer tests for performance.bar_equity (2026-07-31, fix/metrics-bar-equity).

These are pure functions over a bar-level equity series -- no BacktestEngine,
no TradingBot, no backtest run. Every expected value below is either hand-
computable by a single division (max_drawdown_pct) or derived independently
via Python's stdlib `statistics` module rather than typed out as a decimal
literal, so a slip in the implementation can't accidentally match a slip in
the expected value.

See performance/metrics.py's calculate_max_drawdown/calculate_sharpe_ratio
for the trade-exit equivalents this module deliberately does NOT reuse: those
operate on a ~24-point per-trade curve; this operates on the full per-bar
portfolio_states series.
"""
import math
import statistics
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from performance.bar_equity import (
    daily_returns,
    exposure_pct,
    max_drawdown_pct,
    sharpe_ratio_daily,
    sortino_ratio_daily,
    turnover,
)


def _equity_from_returns(returns, start=1000.0):
    """Compound `returns` onto `start` -- avoids hand-typing equity values
    that could silently disagree with the returns used to derive `expected`."""
    equity = [start]
    for r in returns:
        equity.append(equity[-1] * (1 + r))
    return equity


def _daily_index(n):
    return pd.date_range("2024-01-01", periods=n, freq="D")


# ---------------------------------------------------------------------------
# max_drawdown_pct
# ---------------------------------------------------------------------------

def test_max_drawdown_single_drawdown_and_partial_recovery():
    """5-bar series, one drawdown, partial recovery before the end.
    Peak 1100 at bar 1, trough 900 at bar 2: (900-1100)/1100 = -18.181818...%
    """
    equity = pd.Series([1000.0, 1100.0, 900.0, 950.0, 1000.0])
    result = max_drawdown_pct(equity)
    assert abs(result - (-200.0 / 1100.0 * 100)) < 1e-9


def test_max_drawdown_flat_series_is_zero():
    equity = pd.Series([1000.0] * 5)
    assert max_drawdown_pct(equity) == 0.0


def test_max_drawdown_ending_at_final_bar_no_recovery():
    """Trough IS the last point -- guards an off-by-one that excludes the
    final row from the running-max/drawdown window.
    Peak 1200, trough 800 at the last bar: (800-1200)/1200 = -33.333...%
    """
    equity = pd.Series([1000.0, 1200.0, 800.0])
    result = max_drawdown_pct(equity)
    assert abs(result - (-400.0 / 1200.0 * 100)) < 1e-9


def test_max_drawdown_empty_series_is_zero():
    assert max_drawdown_pct(pd.Series([], dtype=float)) == 0.0


def test_max_drawdown_uses_running_max_not_global_max():
    """Discriminates a running-max (correct) implementation from one that
    divides by the series' GLOBAL max throughout (a look-ahead bug: it would
    use a peak that hasn't happened yet at the point of the trough).

    equity=[1000, 800, 2000]: the trough at 800 happens BEFORE the eventual
    global max of 2000. Running max at the trough is 1000 (the only peak seen
    so far) -> (800-1000)/1000 = -20.0%. A global-max implementation would
    wrongly use 2000 -> (800-2000)/2000 = -60.0%. Neither of this file's
    other maxDD fixtures can catch this: in both, the peak occurs before the
    trough with nothing larger appearing afterward, so running-max and
    global-max coincide there by construction.
    """
    equity = pd.Series([1000.0, 800.0, 2000.0])
    result = max_drawdown_pct(equity)
    assert abs(result - (-200.0 / 1000.0 * 100)) < 1e-9  # -20.0, not -60.0


# ---------------------------------------------------------------------------
# sharpe_ratio_daily / sortino_ratio_daily
# ---------------------------------------------------------------------------

def test_sharpe_ratio_daily_known_returns():
    """returns=[0.02, 0.04, 0.03] -> mean=0.03, sample std=0.01 exactly ->
    sharpe = 3.0 * sqrt(365). Expected computed via `statistics` (an
    independent implementation), not typed out as a decimal."""
    returns = [0.02, 0.04, 0.03]
    equity = pd.Series(_equity_from_returns(returns))
    timestamps = pd.Series(_daily_index(len(equity)))
    result = sharpe_ratio_daily(equity, timestamps)
    expected = statistics.mean(returns) / statistics.stdev(returns) * math.sqrt(365)
    assert abs(result - expected) < 1e-6


def test_sharpe_ratio_daily_zero_mean_nonzero_variance_is_exactly_zero():
    """returns=[+0.10, -0.10] -> mean=0 exactly, std>0 (not the degenerate
    guard) -> sharpe must be exactly 0.0, distinct from the zero-std guard
    path below."""
    returns = [0.10, -0.10]
    equity = pd.Series(_equity_from_returns(returns))
    timestamps = pd.Series(_daily_index(len(equity)))
    result = sharpe_ratio_daily(equity, timestamps)
    assert abs(result - 0.0) < 1e-9


def test_sharpe_ratio_daily_flat_series_returns_zero():
    """Zero-variance guard: matches EnhancedPerformanceTracker.calculate_sharpe_ratio's
    own convention (metrics.py:1490-1491) of returning 0.0, never NaN/inf."""
    equity = pd.Series([1000.0] * 5)
    timestamps = pd.Series(_daily_index(5))
    assert sharpe_ratio_daily(equity, timestamps) == 0.0


def test_sharpe_ratio_daily_single_bar_returns_zero():
    """Fewer than 2 daily returns -- can't compute a std, must not raise."""
    equity = pd.Series([1000.0])
    timestamps = pd.Series(_daily_index(1))
    assert sharpe_ratio_daily(equity, timestamps) == 0.0


def test_sortino_ratio_daily_known_downside():
    """returns=[0.05,-0.01,-0.02,-0.03,0.04]. Textbook (target-0) downside
    deviation: sqrt(mean(min(r,0)^2)) over ALL 5 returns, not the sample std
    of the 3 negative ones alone -- deliberately discriminates the two
    conventions: the old (rejected) sample-std-of-negatives formula would give
    0.6*sqrt(365) =~ 11.46 here; the textbook formula gives a different value,
    computed independently below via plain Python, not pandas."""
    returns = [0.05, -0.01, -0.02, -0.03, 0.04]
    equity = pd.Series(_equity_from_returns(returns))
    timestamps = pd.Series(_daily_index(len(equity)))
    result = sortino_ratio_daily(equity, timestamps)
    downside_deviation = math.sqrt(statistics.mean(min(r, 0.0) ** 2 for r in returns))
    expected = statistics.mean(returns) / downside_deviation * math.sqrt(365)
    assert abs(result - expected) < 1e-6
    # the old (rejected) formula's answer must NOT match -- proves this fixture
    # actually discriminates between the two conventions, not just coincidence
    old_formula = statistics.mean(returns) / statistics.stdev([r for r in returns if r < 0]) * math.sqrt(365)
    assert abs(result - old_formula) > 1.0


def test_sortino_ratio_daily_no_downside_returns_zero():
    """All-positive returns -> min(r,0)=0 for every return -> downside
    deviation computes to exactly 0 -> guarded 0.0, not NaN."""
    returns = [0.02, 0.04, 0.03]
    equity = pd.Series(_equity_from_returns(returns))
    timestamps = pd.Series(_daily_index(len(equity)))
    assert sortino_ratio_daily(equity, timestamps) == 0.0


def test_sortino_ratio_daily_flat_series_returns_zero():
    equity = pd.Series([1000.0] * 5)
    timestamps = pd.Series(_daily_index(5))
    assert sortino_ratio_daily(equity, timestamps) == 0.0


def test_sharpe_resample_multiple_bars_per_day_asserts_real_value_not_a_guard():
    """3 days x 2 bars/day -- enough daily returns (2) to escape the <2-return
    guard, so this actually exercises resample('D').last() rather than just
    proving the function doesn't raise. A prior version of this test used
    only 3 bars total (1 daily return), which always hit the guard and so
    could never tell a correct .last() resample apart from a wrong .first()
    or .mean() -- that gap is why this fixture exists.

    equity=[1000,1050, 1100,1210, 1300,1400], two bars per day for 3 days.
    resample('D').last() -> daily closes [1050, 1210, 1400] (the LAST bar of
    each day, not the first: a .first() bug would see [1000, 1100, 1300]
    instead and compute a different, wrong sharpe here).
    """
    equity = pd.Series([1000.0, 1050.0, 1100.0, 1210.0, 1300.0, 1400.0])
    timestamps = pd.Series([
        pd.Timestamp("2024-01-01 00:00"), pd.Timestamp("2024-01-01 12:00"),
        pd.Timestamp("2024-01-02 00:00"), pd.Timestamp("2024-01-02 12:00"),
        pd.Timestamp("2024-01-03 00:00"), pd.Timestamp("2024-01-03 12:00"),
    ])
    daily_closes = [1050.0, 1210.0, 1400.0]
    returns = [daily_closes[i + 1] / daily_closes[i] - 1 for i in range(len(daily_closes) - 1)]

    result = sharpe_ratio_daily(equity, timestamps)
    expected = statistics.mean(returns) / statistics.stdev(returns) * math.sqrt(365)
    assert abs(result - expected) < 1e-6

    # A .first()-resample bug would use [1000, 1100, 1300] instead -- a
    # materially different sharpe. Confirms this fixture actually discriminates.
    first_bug_closes = [1000.0, 1100.0, 1300.0]
    first_bug_returns = [
        first_bug_closes[i + 1] / first_bug_closes[i] - 1 for i in range(len(first_bug_closes) - 1)
    ]
    first_bug_expected = (
        statistics.mean(first_bug_returns) / statistics.stdev(first_bug_returns) * math.sqrt(365)
    )
    assert abs(result - first_bug_expected) > 1.0


def test_daily_returns_resamples_to_last_close_of_each_day():
    """Direct known-answer test of the now-public daily_returns helper itself
    (used by both sharpe_ratio_daily and sortino_ratio_daily, and by
    build_bar_equity for n_daily_returns/n_downside_days)."""
    equity = pd.Series([1000.0, 1050.0, 1100.0, 1210.0, 1300.0, 1400.0])
    timestamps = pd.Series([
        pd.Timestamp("2024-01-01 00:00"), pd.Timestamp("2024-01-01 12:00"),
        pd.Timestamp("2024-01-02 00:00"), pd.Timestamp("2024-01-02 12:00"),
        pd.Timestamp("2024-01-03 00:00"), pd.Timestamp("2024-01-03 12:00"),
    ])
    result = daily_returns(equity, timestamps)
    assert len(result) == 2
    assert abs(result.iloc[0] - (1210.0 / 1050.0 - 1)) < 1e-9
    assert abs(result.iloc[1] - (1400.0 / 1210.0 - 1)) < 1e-9


def test_daily_returns_sorts_out_of_order_input():
    """Row order is not trusted -- an out-of-order (equity, timestamps) pair
    must resample identically to the sorted version. Guards the class of bug
    a caller who doesn't pre-sort would otherwise hit silently."""
    sorted_equity = pd.Series([1000.0, 1100.0, 1200.0])
    sorted_timestamps = pd.Series(_daily_index(3))
    shuffled_equity = pd.Series([1100.0, 1000.0, 1200.0])
    shuffled_timestamps = pd.Series([sorted_timestamps[1], sorted_timestamps[0], sorted_timestamps[2]])

    expected = daily_returns(sorted_equity, sorted_timestamps)
    actual = daily_returns(shuffled_equity, shuffled_timestamps)
    assert list(actual.values) == list(expected.values)


# ---------------------------------------------------------------------------
# turnover / exposure_pct
# ---------------------------------------------------------------------------

def test_turnover_sums_executed_allocation_deltas():
    """post=[0, 0.5, 0], previous=[0, 0, 0.5] -> |0.5-0| + |0-0.5| = 1.0.
    Uses the two allocation columns directly, not the raw allocation_change
    field, which also includes rejected/unexecuted rebalance attempts."""
    post = pd.Series([0.0, 0.5, 0.0])
    previous = pd.Series([0.0, 0.0, 0.5])
    assert abs(turnover(post, previous) - 1.0) < 1e-9


def test_turnover_zero_when_allocation_never_changes():
    post = pd.Series([0.0, 0.0, 0.0])
    previous = pd.Series([0.0, 0.0, 0.0])
    assert turnover(post, previous) == 0.0


def test_exposure_pct_share_of_nonzero_bars():
    """1 of 3 bars has a nonzero post-rebalance allocation -> 33.333...%"""
    post = pd.Series([0.0, 0.5, 0.0])
    result = exposure_pct(post)
    assert abs(result - (100.0 / 3.0)) < 1e-9


def test_exposure_pct_zero_when_always_flat():
    post = pd.Series([0.0, 0.0, 0.0])
    assert exposure_pct(post) == 0.0


def test_exposure_pct_empty_series_is_zero():
    assert exposure_pct(pd.Series([], dtype=float)) == 0.0
