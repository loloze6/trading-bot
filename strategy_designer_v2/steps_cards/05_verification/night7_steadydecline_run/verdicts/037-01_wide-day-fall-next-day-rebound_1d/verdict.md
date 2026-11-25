---
plan: 037-01_wide-day-fall-next-day-rebound_1d
idea: 037-01_wide-day-fall-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: timing gain before costs, per-day mean across coins: 0.000740075; t of the mean over days: 2.37149 (threshold: confirm if t >= 2 and mean > 0 (with supporting check); reject if t <= -2)
- Supporting check: upper minus lower half (median post_pipeline_value) mean next-day excess return, Welch t: 0.00516431, passed: True
- Counts: bars with forecast > 0: 8605, distinct days: 2219, days in main measure: 2898
- Decided by: Main measure t >= 2 with a positive mean, and the supporting check passes.
- Reading: Days are UTC calendar days of the bar timestamp, the coin's mean is over all its within-window next-day returns, the median split puts values above the median in the upper half and the rest in the lower, and the plan's 'fewer is inconclusive' minimum is reported as not observable.
- Size: unusual move +0.18 % (t 1.41, the cases of one day together: 1631 days) per case over 1 bars, 0.039 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.30 %; 5337 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0005394 on the check folds against +0.0007401 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/037-01_wide-day-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/037-01_wide-day-fall-next-day-rebound_1d`
Measure: `measure.py`
