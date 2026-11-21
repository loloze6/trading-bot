---
plan: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal
fit: exact
status: confirmed
---
Situation check: 95 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-bar coin return less coin mean daily return, on forecast: 0.000521769; OLS t of slope: 4.26575 (threshold: confirm: slope > 0 with t >= 2 (and supporting check passes); reject: slope < 0 with t <= -2)
- Supporting check: book timing gain before costs (mean daily) > 0: 0.000352207, passed: True
- Counts: bars with a non-zero forecast: 5842, bars in the regression: 5794, book days: 2898
- Decided by: The slope is positive with t >= 2 and the timing gain before costs is above 0.
- Reading: The situation is any bar with a non-zero day's move (sign of the raw fade component, else the price return) and the expected side is opposite to that move; the regression is OLS with an intercept on every bar with a next-bar return inside its window; the book's timing gain before costs is the position held after bar t-1's trade times (coin return on bar t minus the coin's mean daily return over all windows), averaged across coins each day and then over days.
- Size: unusual move +0.25 % per case over 1 bars, 0.062 of the coin's usual move (4.01 %); normal drift in its direction -0.01 %, total +0.25 %; 2446 cases
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d`
Measure: `measure.py`
