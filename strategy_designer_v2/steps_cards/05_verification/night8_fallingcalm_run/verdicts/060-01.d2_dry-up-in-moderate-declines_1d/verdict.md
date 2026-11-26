---
plan: 060-01.d2_dry-up-in-moderate-declines_1d
idea: 060-01.d2_dry-up-in-moderate-declines
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move of the short cases, drift removed: 0.00912594; t of the mean, cases of one day taken together: 1.69807 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases)
- Supporting check: mean unusual move, cases with |forecast| above median minus below median: 0.00594155, passed: True
- Counts: cases: 487, days: 377
- Decided by: t is between -2 and 2.
- Reading: Falling profile taken as the 60-bar price evolution in percent below -10 (the detector's regime where 60 past bars are not in the window) and the dry-up as a raw component value above 0; a case is the first bet (short forecast rising at least 2 points from its lowest level since the last bet, from 0 after flat) in each 5-bar grid cell from each window's first row, cases without 5 bars ahead in the window are dropped, the drift is the coin's mean non-overlapping 5-bar return over all windows, the day-clustered t uses summed deviations per day with a D/(D-1) correction, and cases with |forecast| equal to the median are in neither group.
- Size: unusual move +0.91 % (t 1.70, the cases of one day together: 377 days) per case over 5 bars, 0.082 of the coin's usual move (10.60 %); normal drift in its direction -0.60 %, total +0.32 %; 487 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-01.d2_dry-up-in-moderate-declines_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-01.d2_dry-up-in-moderate-declines_1d`
Measure: `measure.py`
