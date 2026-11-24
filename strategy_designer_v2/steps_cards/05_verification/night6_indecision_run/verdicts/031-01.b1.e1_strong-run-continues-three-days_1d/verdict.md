---
plan: 031-01.b1.e1_strong-run-continues-three-days_1d
idea: 031-01.b1.e1_strong-run-continues-three-days
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-bar return on forecast (non-overlapping grid, pooled): 0.00072065; OLS slope t: 4.38372 (threshold: t >= 2 confirms (with the supporting check), t <= -2 rejects, otherwise inconclusive)
- Supporting check: forecast-weighted mean excess 3-bar return on grid bars with forecast > 0: 0.00672863, passed: True
- Counts: grid bars with a forecast above 0: 2907, grid bars: 5723
- Decided by: The slope's t is >= 2 and the forecast-weighted mean excess return on positive-forecast grid bars is above 0.
- Reading: Grid bars at positions 0, 3, 6, ... of each window, dropping those without a bar t+3 in the window; the coin's mean 3-bar return is the mean of its grid returns over all its windows; the slope is an OLS with intercept and its ordinary t; the 200 minimum counts grid bars with forecast > 0 and a valid 3-bar return and, as a minimum count, gives 'not observable' when not reached.
- Size: unusual move +0.19 % (t 0.81, the cases of one day together: 1195 days) per case over 3 bars, 0.023 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.54 %; 2730 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.e1_strong-run-continues-three-days_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1.e1_strong-run-continues-three-days_1d`
Measure: `measure.py`
