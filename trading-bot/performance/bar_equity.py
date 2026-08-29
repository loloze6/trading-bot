"""
Off-by-default, additive bar-level equity metrics (2026-07-31, fix/metrics-bar-equity).

core.sharpe / core.max_drawdown_pct (see EnhancedPerformanceTracker.calculate_max_drawdown
and .calculate_sharpe_ratio in performance/metrics.py) are computed from a per-TRADE
equity curve -- 24 points for the reference window, one per completed trade -- and
Sharpe's daily series is built by summing trade returns per exit date and filling every
non-trading calendar day with a synthetic 0.0 return. Both understate risk: the trade-exit
curve can only ever sample equity at 24 points, never the trough of a trade that hasn't
exited yet or the drawdown between exits, and the 0-filled non-trading days dilute
volatility with days that never happened as a flat return.

These functions instead take the full per-bar equity series (portfolio_states.csv's
postRebalance_total_value column -- the value AFTER each bar's rebalance executes, which
is what actually carries forward into the next bar; see build_bar_equity in
reporting/run_artifact.py for why that column and not total_portfolio_value). Sharpe and
Sortino resample that series to daily closes (last bar of each calendar day) rather than
trade-exit dates, so no day is ever fabricated as a flat 0.0 -- a day with no bar in it
(a real data gap) is simply absent from the resampled series, not zero-filled.

Every function here is pure: no BacktestEngine, no TradingBot, no I/O. All of them
mirror EnhancedPerformanceTracker.calculate_sharpe_ratio's own convention of returning
0.0 (never NaN or inf) when volatility is undefined -- zero variance, or fewer than two
observations.
"""

import math

import pandas as pd


def max_drawdown_pct(equity: pd.Series) -> float:
    """Peak-to-trough drawdown over the full series, in percent (<= 0)."""
    if len(equity) == 0:
        return 0.0
    running_max = equity.expanding().max()
    drawdown = (equity - running_max) / running_max
    return float(drawdown.min() * 100)


def daily_returns(equity: pd.Series, timestamps: pd.Series) -> pd.Series:
    """Resample `equity` to one value per calendar day (the day's last bar,
    matching build_bar_equity's post-warmup bar series) and return the
    day-over-day pct change. Sorted by timestamp first -- the caller's row
    order is not trusted, since a running-max/resample computed over an
    out-of-order series is silently wrong rather than erroring.

    A calendar day with no bar in it is absent from the result, never
    fabricated as a 0.0 return. Consequence, not a defect: the return spanning
    a gap is computed between the last bar before it and the first bar after,
    however many real days that gap covers, but is then treated -- and
    annualized -- as a single day's return. Dropping the day is still the
    right call over fabricating a flat 0.0 for it; the gap's true multi-day
    span is just not separately recoverable from this series.
    """
    daily = pd.Series(equity.values, index=pd.to_datetime(timestamps.values)).sort_index().resample("D").last().dropna()
    return daily.pct_change().dropna()


def sharpe_ratio_daily(equity: pd.Series, timestamps: pd.Series) -> float:
    """Annualized Sharpe (sqrt(365)) from `equity` resampled to daily closes."""
    daily_ret = daily_returns(equity, timestamps)
    std = daily_ret.std()
    if len(daily_ret) < 2 or std == 0 or pd.isna(std):
        return 0.0
    return float(daily_ret.mean() / std * math.sqrt(365))


def sortino_ratio_daily(equity: pd.Series, timestamps: pd.Series) -> float:
    """Same daily basis as sharpe_ratio_daily. Downside deviation is the
    textbook target-0 semi-deviation: sqrt(mean(min(r, 0)^2)) over ALL daily
    returns, not the sample std of the negative-return subset alone -- the
    standard Sortino definition measures deviation below a target return
    (0 here), not the spread among losing days."""
    daily_ret = daily_returns(equity, timestamps)
    if len(daily_ret) < 2:
        return 0.0
    downside_deviation = math.sqrt((daily_ret.clip(upper=0.0) ** 2).mean())
    if downside_deviation == 0 or pd.isna(downside_deviation):
        return 0.0
    return float(daily_ret.mean() / downside_deviation * math.sqrt(365))


def turnover(post_rebalance_allocation: pd.Series, previous_allocation: pd.Series) -> float:
    """Sum of |executed allocation change| per bar. Uses the two allocation
    columns directly rather than the raw allocation_change field, which also
    counts rebalance attempts the risk manager rejected -- never executed,
    so they moved no capital."""
    return float((post_rebalance_allocation - previous_allocation).abs().sum())


def exposure_pct(post_rebalance_allocation: pd.Series) -> float:
    """Share of bars holding a nonzero post-rebalance allocation, in percent."""
    if len(post_rebalance_allocation) == 0:
        return 0.0
    return float((post_rebalance_allocation != 0.0).mean() * 100)
