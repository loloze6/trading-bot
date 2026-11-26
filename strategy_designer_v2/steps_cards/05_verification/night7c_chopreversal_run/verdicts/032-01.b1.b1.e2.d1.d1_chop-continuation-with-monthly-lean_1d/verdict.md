---
plan: 032-01.b1.b1.e2.d1.d1_chop-continuation-with-monthly-lean_1d
idea: 032-01.b1.b1.e2.d1.d1_chop-continuation-with-monthly-lean
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-bar move of cases, in forecast direction: 0.0105851; day-clustered t: 2.74512 (threshold: confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move of |forecast| above median minus at or below median: 0.00937188, passed: True
- Counts: distinct case days: 1043, cases: 1758
- Decided by: Mean unusual move above 0 with t >= 2 and the large-minus-small difference above 0.
- Reading: Active bars whose 30-bar efficiency ratio or 30-bar return cannot be computed inside their window (first 30 recorded bars) are left out of the situation check; a case is the first bet (forecast rise of at least 2 points on its side) in each 7-bar grid cell counted from the window's first row; the drift is the coin's mean 7-bar return on that grid over all its windows; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; large cases are |forecast| strictly above the cases' median.
- Size: unusual move +1.06 % (t 2.75, the cases of one day together: 1043 days) per case over 7 bars, 0.079 of the coin's usual move (12.44 %); normal drift in its direction -0.03 %, total +1.03 %; 1758 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0006365 on the check folds against +0.01059 on every fold
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1.d1_chop-continuation-with-monthly-lean_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1.d1_chop-continuation-with-monthly-lean_1d`
Measure: `measure.py`
