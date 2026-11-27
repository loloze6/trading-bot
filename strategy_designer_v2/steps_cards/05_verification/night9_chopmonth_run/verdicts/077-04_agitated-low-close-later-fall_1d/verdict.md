---
plan: 077-04_agitated-low-close-later-fall_1d
idea: 077-04_agitated-low-close-later-fall
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 6-bar move of short cases (short direction, coin drift removed): 0.00515388; day-clustered t of the mean: 0.925389 (threshold: t >= 2 confirms (with supporting difference > 0); t <= -2 rejects; at least 30 distinct case days)
- Supporting check: upper-half minus lower-half mean unusual move by |forecast| at entry: 0.00615296, passed: True
- Counts: distinct case days: 736, cases: 1907
- Decided by: The t of the mean unusual move lies between -2 and 2, which the plan calls inconclusive.
- Reading: The situation is checked as previous-day close location (recorded raw value, else rebuilt from prices) >= 0.75 with a negative forecast, the agitated profile not being recomputable from the record; a case is the first short bet (rise of -forecast by >= 2 from its low since the last bet) in each 6-bar grid cell of a window, its return taken from that bar's close over 6 bars inside the window, the drift is the coin's mean 6-bar return on the non-overlapping grid of all its windows, the t is day-clustered (deviations summed per UTC day), and the median split puts |forecast| above the median in the upper half and at or below it in the lower half.
- Size: unusual move +0.52 % (t 0.93, the cases of one day together: 736 days) per case over 6 bars, 0.042 of the coin's usual move (12.40 %); normal drift in its direction -0.86 %, total -0.35 %; 1907 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/077-04_agitated-low-close-later-fall_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/077-04_agitated-low-close-later-fall_1d`
Measure: `measure.py`
