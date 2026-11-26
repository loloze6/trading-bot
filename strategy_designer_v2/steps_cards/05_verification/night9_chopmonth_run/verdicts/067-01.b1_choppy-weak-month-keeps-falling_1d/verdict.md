---
plan: 067-01.b1_choppy-weak-month-keeps-falling_1d
idea: 067-01.b1_choppy-weak-month-keeps-falling
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-bar move of short cases (short direction): 0.0112626; day-clustered t: 2.07863 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: OLS slope of 7-bar excess return on forecast (grid bars, forecast < 0), t: 3.04263, passed: True
- Counts: cases: 1024, distinct days: 624, grid bars with forecast < 0: 633
- Decided by: Mean unusual move above 0 with t >= 2 and the slope is positive with t >= 2.
- Reading: The choppy profile is the 'unknown' regime column; a case is the first short bet in each 7-bar grid cell of a window, drift is the coin's mean non-overlapping 7-bar return over all windows, the clustered t uses a G/(G-1) correction, and the slope's t is the ordinary pooled OLS t.
- Size: unusual move +1.13 % (t 2.08, the cases of one day together: 624 days) per case over 7 bars, 0.071 of the coin's usual move (14.34 %); normal drift in its direction -1.13 %, total -0.01 %; 1024 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.00688 on the check folds against +0.01126 on every fold
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1_choppy-weak-month-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1_choppy-weak-month-keeps-falling_1d`
Measure: `measure.py`
