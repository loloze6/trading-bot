---
plan: 002-03_price-cross-above-long-sma.b1_cross-with-rising-average_1d
idea: 002-03_price-cross-above-long-sma.b1_cross-with-rising-average
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 20-bar forward return of active cases (forecast > 0) over coin holding mean: 0.0112688; t of the mean: 0.584676 (threshold: confirm: mean > 0 with t >= 2 (and slope > 0); reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of excess 20-bar return on forecast, active cases: 0.00598025, passed: True
- Counts: active non-overlapping cases: 322
- Decided by: The main t lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: Holding is each coin's mean 20-bar return over the same non-overlapping grid samples of all its windows; a grid bar counts only if t+20 lies in the same window; the plan's 'fewer than 30 active cases' minimum is treated as not observable; the situation is checked on regime == 'trending' plus the recorded ma_slope raw value > 0.
- Size: unusual move +2.01 % per case over 20 bars, 0.054 of the coin's usual move (21.24 %); normal drift in its direction +3.00 %, total +5.01 %; 236 cases
Plan: `steps_cards/03_test_plan/plans/002-03_price-cross-above-long-sma.b1_cross-with-rising-average_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.b1_cross-with-rising-average_1d`
Measure: `measure.py`
