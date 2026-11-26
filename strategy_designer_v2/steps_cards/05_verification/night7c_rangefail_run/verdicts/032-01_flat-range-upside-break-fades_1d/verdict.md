---
plan: 032-01_flat-range-upside-break-fades_1d
idea: 032-01_flat-range-upside-break-fades
fit: adapted
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 10-bar move (return minus coin drift, fall positive): -0.0434846; t of the mean, cases summed per day: -1.97138 (threshold: t >= 2 (with slope > 0) confirms, t <= -2 rejects, otherwise inconclusive)
- Supporting check: OLS slope of unusual move on raw overshoot: -0.00215805, passed: False
- Counts: cases: 136, distinct days: 118
- Decided by: the t of the mean short-side unusual move lies between -2 and 2
- Reading: the efficiency ratio is rebuilt from closes as |close change over 60 bars| / sum of 60 absolute daily changes, smoothed by a 5-bar mean, and only active bars with enough in-window history to compute it enter the agreement share; a case is the first short bet (forecast rise of at least 2 points on the short side) in each 10-bar grid cell counted from each window's first row, cases without 10 later bars in their window are dropped, the drift is the mean of the coin's non-overlapping 10-bar grid returns over all windows, and fewer than 30 cases or days gives 'not observable' as the workflow's minimum-count rule requires
- Size: unusual move -4.35 % (t -1.98, the cases of one day together: 118 days) per case over 10 bars, -0.228 of the coin's usual move (14.49 %); normal drift in its direction -1.18 %, total -5.53 %; 136 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-01_flat-range-upside-break-fades_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-01_flat-range-upside-break-fades_1d`
Measure: `measure.py`
