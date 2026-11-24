---
plan: 031-01_wide-flat-day-ends-uprun_1d
idea: 031-01_wide-flat-day-ends-uprun
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-day unusual move in the short direction: -0.012447; t of the mean, same-day cases taken together: -0.929333 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean unusual move above minus below the median |forecast|: 0.0490328, passed: True
- Counts: cases: 86, days: 74, active bars: 87
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Active bars whose 5-day return or range ratio cannot be computed inside the record are left out of the agreement share; a case is the first short bet in each 5-bar cell of its window, cases with no full 5-bar return in the window are dropped, the t clusters cases by UTC day, and the supporting check compares cases strictly above with cases strictly below the median |forecast| (ties left out).
- Size: unusual move -1.24 % (t -0.94, the cases of one day together: 74 days) per case over 5 bars, -0.116 of the coin's usual move (10.60 %); normal drift in its direction -0.60 %, total -1.84 %; 86 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01_wide-flat-day-ends-uprun_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01_wide-flat-day-ends-uprun_1d`
Measure: `measure.py`
