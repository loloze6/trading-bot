---
plan: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls_1d
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of excess 10-bar return regressed on forecast, over positive-forecast grid cells: 0.00173951; OLS slope t: 1.56626 (threshold: confirm if slope t >= 2 with mean excess > 0; reject if slope t <= -2; at least 100 cells)
- Supporting check: mean excess 10-bar return over the same cells above 0: 0.00569046, passed: True
- Counts: cells with a positive forecast: 292
- Decided by: a slope t between -2 and 2 is inconclusive.
- Reading: cells are at positions 0, 10, 20, ... of each window with a full 10-bar forward return inside it; each coin's normal drift is the mean of its 10-bar returns over all such cells of all its windows; the regression pools the cells of all coins, and the main measure's value is the slope (excess return per forecast point).
- Size: unusual move -0.20 % per case over 10 bars, -0.013 of the coin's usual move (12.83 %); normal drift in its direction +1.26 %, total +1.06 %; 553 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls_1d.md`
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls_1d`
Measure: `measure.py`
