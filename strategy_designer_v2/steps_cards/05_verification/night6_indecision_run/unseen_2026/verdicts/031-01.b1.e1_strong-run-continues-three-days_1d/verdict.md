---
plan: 031-01.b1.e1_strong-run-continues-three-days_1d
idea: 031-01.b1.e1_strong-run-continues-three-days
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-bar return on forecast (non-overlapping grid, pooled): 0.000563138; OLS slope t: 1.32296 (threshold: t >= 2 confirms (with the supporting check), t <= -2 rejects, otherwise inconclusive)
- Supporting check: forecast-weighted mean excess 3-bar return on grid bars with forecast > 0: 0.00566113, passed: True
- Counts: grid bars with a forecast above 0: 283, grid bars: 624
- Decided by: The slope's t is between -2 and 2.
- Reading: Grid bars at positions 0, 3, 6, ... of each window, dropping those without a bar t+3 in the window; the coin's mean 3-bar return is the mean of its grid returns over all its windows; the slope is an OLS with intercept and its ordinary t; the 200 minimum counts grid bars with forecast > 0 and a valid 3-bar return and, as a minimum count, gives 'not observable' when not reached.
- Size: unusual move -0.38 % (t -0.66, the cases of one day together: 123 days) per case over 3 bars, -0.033 of the coin's usual move (5.48 %); normal drift in its direction +0.05 %, total -0.33 %; 279 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.e1_strong-run-continues-three-days_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.b1.e1_strong-run-continues-three-days_1d`
Measure: `measure.py`
