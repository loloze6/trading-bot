---
plan: 032-01.b1.b1.e1_large-weekly-fall-continues_1d
idea: 032-01.b1.b1.e1_large-weekly-fall-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 7-bar move per case (return minus coin's normal 7-bar drift): -0.0216037; t of the mean, cases of one day taken together: -1.09843 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and deeper half beats shallower half; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: deeper-half minus shallower-half mean unusual move (split at median |forecast|): 0.056198, passed: True
- Counts: cases: 123, days: 68
- Decided by: The t lies between -2 and 2 (or could not be computed) over at least 30 cases.
- Reading: Raw vsr taken from the recorded fall.last_history_value (recomputed from closes with ddof=1 where missing); a case is the first short bet (rise of |forecast| on the short side of at least 2 points from its lowest level since the last bet, reset at 0 after flat or side change) in each 7-bar grid cell from each window's first row, cases without 7 bars ahead in the window are dropped, drift is the coin's mean non-overlapping 7-bar return over all its windows, the day-clustered t uses per-day summed deviations with a G/(G-1) correction, the median split puts |forecast| above the median in the deeper half and at or below it in the shallower half, and fewer than 30 cases gives 'not observable'.
- Size: unusual move -2.16 % (t -1.11, the cases of one day together: 68 days) per case over 7 bars, -0.174 of the coin's usual move (12.44 %); normal drift in its direction -0.91 %, total -3.07 %; 123 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e1_large-weekly-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e1_large-weekly-fall-continues_1d`
Measure: `measure.py`
