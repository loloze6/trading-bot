---
plan: 032-01_choppy-upside-break-fades_1d
idea: 032-01_choppy-upside-break-fades
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move in the short direction over 5 bars, t clustered by day: -0.00870984; t of the mean, cases clustered by day: -0.701913 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on |forecast|: -0.00908295, passed: False
- Counts: cases: 80, distinct days: 67
- Decided by: The t lies between -2 and 2: inconclusive.
- Reading: The choppy profile is read from the recorded regime (bars not vetoed to 'chop'), the 20-day distance from the overshoot component's raw value or else recomputed from prices; a case is the first short bet (forecast rising in size by >= 2 points from its lowest level since the last bet, from 0 after a flat) in each 5-bar grid cell, the normal drift is the mean of the coin's non-overlapping 5-bar grid returns over all windows, the clustered t uses per-day summed deviations with no small-sample correction, and the plan's '<30 cases or days' rule is reported as 'not observable' as the workflow requires for minimum counts.
- Size: unusual move -0.87 % (t -0.70, the cases of one day together: 67 days) per case over 5 bars, -0.045 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total -1.45 %; 80 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/032-01_choppy-upside-break-fades_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/032-01_choppy-upside-break-fades_1d`
Measure: `measure.py`
