---
plan: 077-01_choppy-calm-swing-rise-carries_1d
idea: 077-01_choppy-calm-swing-rise-carries
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-bar move over forecast-rise cases (long): 0.014229; t of the mean, cases grouped by day: 1.27729 (threshold: confirm: mean > 0 with day-grouped t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move above median forecast minus below median forecast > 0: None, passed: False
- Counts: cases: 162, case-days: 140
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Cases are the first long forecast rise of >= 2 points (from its lowest level since the last bet, reset to 0 when flat) in each 7-bar grid cell from each window's first row; the day-grouped t uses the cluster standard error of the mean with deviations summed per UTC day (small-sample factor G/(G-1)); cases equal to the median forecast are left out of both halves of the supporting check; fewer than 30 case-days is reported as not observable.
- Size: unusual move +1.42 % (t 1.28, the cases of one day together: 140 days) per case over 7 bars, 0.087 of the coin's usual move (12.44 %); normal drift in its direction +0.98 %, total +2.40 %; 162 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/077-01_choppy-calm-swing-rise-carries_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/077-01_choppy-calm-swing-rise-carries_1d`
Measure: `measure.py`
