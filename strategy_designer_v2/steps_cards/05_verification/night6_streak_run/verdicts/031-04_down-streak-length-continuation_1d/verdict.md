---
plan: 031-04_down-streak-length-continuation_1d
idea: 031-04_down-streak-length-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 5-bar move of short bets (vs coin's normal 5-bar drift): -0.000582245; t of the mean, same-day cases summed: -0.184695 (threshold: confirm: mean > 0 with t >= 2 over >= 30 distinct days and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 distinct days)
- Supporting check: mean unusual move, |forecast| above median minus at/below median: 0.00147477, passed: True
- Counts: cases: 3143, distinct case days: 1187
- Decided by: The t lies between -2 and 2.
- Reading: A case is the first short bet (|forecast| rising >= 2 points from its lowest short level since the last bet, from 0 after flat/side change) in each 5-bar grid cell from each window's first row, needing 5 bars ahead in its window; the drift is the coin's mean 5-bar return on that grid over all windows; the t uses a day-clustered standard error (deviations summed per UTC day); the median split puts |forecast| above the median in the larger half and at or below in the smaller.
- Size: unusual move -0.06 % (t -0.18, the cases of one day together: 1187 days) per case over 5 bars, -0.005 of the coin's usual move (10.60 %); normal drift in its direction -0.66 %, total -0.72 %; 3143 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-04_down-streak-length-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-04_down-streak-length-continuation_1d`
Measure: `measure.py`
