---
plan: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high_1d
idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-removed 5-bar return on forecast (pooled breakout cases): 0.000887544; OLS slope t: 0.37213 (threshold: confirm if slope t >= 2 (with supporting check), reject if slope t <= -2, at least 30 cases)
- Supporting check: mean drift-removed 5-bar return of breakout cases above 0: 0.00813336, passed: True
- Counts: breakout cases: 175, active bars: 908
- Decided by: The slope t lies between -2 and 2.
- Reading: Grid bars are positions 0,5,10,... of each window with a full 5-bar return inside it; the coin's mean 5-bar return is the mean over all its grid returns across windows; the regressor is post_pipeline_value (forecast where it is missing); the situation check uses the raw distance above 0 with a positive forecast.
- Size: unusual move +3.17 % per case over 5 bars, 0.266 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +3.76 %; 260 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high_1d`
Measure: `measure.py`
