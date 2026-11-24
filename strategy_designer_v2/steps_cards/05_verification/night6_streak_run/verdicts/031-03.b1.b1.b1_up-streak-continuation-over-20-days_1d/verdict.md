---
plan: 031-03.b1.b1.b1_up-streak-continuation-over-20-days_1d
idea: 031-03.b1.b1.b1_up-streak-continuation-over-20-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 20-bar move of cases (forecast rise >= 2), before costs: 0.0180974; t of the mean, cases summed per day: 1.29429 (threshold: confirm: mean > 0 with t >= 2 and top-third minus bottom-third > 0; reject: mean < 0 with t <= -2)
- Supporting check: top-third minus bottom-third mean unusual move (by forecast size): 0.00844885, passed: True
- Counts: cases: 1071, distinct case days: 449
- Decided by: The t lies between -2 and 2 (or cannot be computed).
- Reading: Situation = 30-day close return > 0 (recomputed inside each window, active bars of a window's first 30 rows left out of the check) and raw streak rank > 0, expected side long; a case is the first long bet (forecast rise >= 2 from its low since the last bet, from 0 after a flat) in each 20-bar grid cell of a window, its return taken from that bar's close 20 bars on inside the window, the drift is the mean non-overlapping 20-bar grid return over all the coin's windows, t uses day-clustered deviations, and the thirds are the first and last n//3 cases sorted by forecast value at the signal bar.
- Size: unusual move +1.81 % (t 1.30, the cases of one day together: 449 days) per case over 20 bars, 0.060 of the coin's usual move (23.14 %); normal drift in its direction +3.08 %, total +4.89 %; 1071 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.b1_up-streak-continuation-over-20-days_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1.b1.b1_up-streak-continuation-over-20-days_1d`
Measure: `measure.py`
