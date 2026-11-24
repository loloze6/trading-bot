---
plan: 032-01_choppy-agitated-weekly-rise-reverts_1d
idea: 032-01_choppy-agitated-weekly-rise-reverts
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Pearson correlation of forecast with next 7-bar return minus normal 7-bar drift (non-overlapping grid, forecast < 0): -0.134985; t of Pearson correlation: -1.29957 (threshold: confirm: correlation positive with t >= 2 and supporting check passes; reject: negative with t <= -2)
- Supporting check: mean unusual move in the signal's direction (fall beyond drift): 0.00120909, passed: True
- Counts: grid cases with a forecast below 0: 93
- Decided by: The correlation t lies between -2 and 2.
- Reading: Situation taken as a positive raw 7-day return (recorded rise7 value, recomputed from closes where missing) with a short forecast, profile not part of the check; drift is each coin's mean non-overlapping 7-bar return over all its windows; grid cases are grid bars with forecast < 0 and a full 7-bar return inside the window; the plan's 'fewer than 30 grid cases' minimum is applied as 'not observable'.
- Size: unusual move -0.69 % (t -0.83, the cases of one day together: 160 days) per case over 7 bars, -0.048 of the coin's usual move (12.44 %); normal drift in its direction -0.98 %, total -1.67 %; 195 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/032-01_choppy-agitated-weekly-rise-reverts_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/032-01_choppy-agitated-weekly-rise-reverts_1d`
Measure: `measure.py`
