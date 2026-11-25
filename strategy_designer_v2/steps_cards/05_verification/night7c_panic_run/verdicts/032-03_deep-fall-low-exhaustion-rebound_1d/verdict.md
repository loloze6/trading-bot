---
plan: 032-03_deep-fall-low-exhaustion-rebound_1d
idea: 032-03_deep-fall-low-exhaustion-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of long cases: 0.00591791; t of the mean, cases grouped by day: 0.558584 (threshold: confirm: mean > 0 with t >= 2 (and correlation > 0); reject: mean < 0 with t <= -2)
- Supporting check: Spearman(forecast, unusual move) > 0: 0.0659508, passed: True
- Counts: cases: 236, cases on distinct days: 155
- Decided by: t lies between -2 and 2: inconclusive rule.
- Reading: The 365-bar range ratio is taken from the recorded regime (not rebuildable in ~120-bar windows); a case is the first long bet (forecast rise >= 2 from its low since the last bet, reset at flat) in each 5-bar grid cell counted from each window's first row, needing 5 bars ahead in the window; the drift is the mean of the coin's non-overlapping 5-bar grid returns over all windows; the t clusters deviations summed per day with a G/(G-1) correction; 'at least 30 cases on distinct days' is read as at least 30 distinct case days, and fewer is reported as not observable.
- Size: unusual move +0.59 % (t 0.56, the cases of one day together: 155 days) per case over 5 bars, 0.070 of the coin's usual move (10.60 %); normal drift in its direction +0.64 %, total +1.23 %; 236 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-03_deep-fall-low-exhaustion-rebound_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-03_deep-fall-low-exhaustion-rebound_1d`
Measure: `measure.py`
