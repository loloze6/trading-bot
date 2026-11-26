---
plan: 041-03_agitated-fall-drop-vs-range-rebound_1d
idea: 041-03_agitated-fall-drop-vs-range-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return (vs coin's all-window mean daily return): 0.0106962; t of weighted mean, same-day cases summed: 3.63903 (threshold: confirm: mean > 0 with t >= 2 and positive slope; reject: mean < 0 with t <= -2; min 100 cases on 60 distinct days)
- Supporting check: OLS slope of next-day excess return on forecast: 0.000877246, passed: True
- Counts: cases: 1468, distinct days: 702
- Decided by: Weighted mean excess next-day return above 0 with t >= 2 and a positive slope on forecast.
- Reading: Profile bars are those with recorded regime 'unknown' (the config's only active regime); cases are every in-profile bar with forecast > 0 and a next close in the same window; the coin's mean is the mean of all its within-window 1-bar returns; the t uses per-day sums of weighted deviations from the weighted mean (cluster-by-day standard error); the slope is ordinary least squares on all cases; the plan's minimum counts lead to 'not observable' when unmet.
- Size: unusual move +0.98 % (t 3.39, the cases of one day together: 511 days) per case over 1 bars, 0.211 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +1.11 %; 1040 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004847 on the check folds against +0.0107 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/041-03_agitated-fall-drop-vs-range-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/041-03_agitated-fall-drop-vs-range-rebound_1d`
Measure: `measure.py`
