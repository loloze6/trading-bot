---
plan: 058-01.g2.b1.d2.b1.d2.g1_multi-day-rally-give-back_1d
idea: 058-01.g2.b1.d2.b1.d2.g1_multi-day-rally-give-back
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move in the short's direction (return minus coin's normal 3-day drift, x -1): 0.00980749; t of the mean, cases of one day taken together: 1.71039 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 cases on distinct days)
- Supporting check: mean unusual move of larger-|forecast| half minus smaller half: 0.00895809, passed: True
- Counts: cases: 779, cases on distinct days: 256
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Profile read from the recorded regime 'unknown' (no chop veto) and the rise from the raw component > 0; cases are grid bars 0,3,6,... of each window with forecast < 0 and a 3-bar return inside the window; drift is the coin's mean non-overlapping 3-day return over all windows; the t uses deviations summed per UTC day with a D/(D-1) correction; the larger half is |forecast| strictly above the median and the smaller half at or below it; the minimum of 30 is applied to the number of distinct days of the cases.
- Size: unusual move +0.70 % (t 1.46, the cases of one day together: 391 days) per case over 3 bars, 0.075 of the coin's usual move (8.85 %); normal drift in its direction -0.44 %, total +0.26 %; 952 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d2.b1.d2.g1_multi-day-rally-give-back_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d2.g1_multi-day-rally-give-back_1d`
Measure: `measure.py`
