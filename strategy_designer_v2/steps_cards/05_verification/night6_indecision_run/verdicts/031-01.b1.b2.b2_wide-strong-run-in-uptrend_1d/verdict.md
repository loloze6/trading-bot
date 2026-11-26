---
plan: 031-01.b1.b2.b2_wide-strong-run-in-uptrend_1d
idea: 031-01.b1.b2.b2_wide-strong-run-in-uptrend
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move of long cases (return minus coin's normal 3-day drift): 0.00202834; t of the mean, same-day cases pooled: 0.67968 (threshold: confirm: mean > 0 with t >= 2 (and upper-minus-lower > 0); reject: mean < 0 with t <= -2)
- Supporting check: upper-half minus lower-half mean unusual move (split at median forecast): 0.00893521, passed: True
- Counts: cases: 1484, distinct days: 825
- Decided by: The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive.
- Reading: The 60-day and 5-day returns are recomputed from closes inside each window, and on bars too early in a window for that the recorded regime 'trending' stands for the detector's decision; a case is the first long bet (forecast rise of at least 2 points from its lowest level since the last bet, from 0 after a flat) in each 3-bar grid cell of a window with a 3-bar forward return inside the window; the normal drift is the coin's mean non-overlapping 3-bar return over all its windows; the day-pooled t uses the per-day sums of deviations with a D/(D-1) correction; the upper half is forecast above the median, the lower half forecast at or below it.
- Size: unusual move +0.20 % (t 0.68, the cases of one day together: 825 days) per case over 3 bars, 0.020 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.56 %; 1484 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b2_wide-strong-run-in-uptrend_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1.b2.b2_wide-strong-run-in-uptrend_1d`
Measure: `measure.py`
