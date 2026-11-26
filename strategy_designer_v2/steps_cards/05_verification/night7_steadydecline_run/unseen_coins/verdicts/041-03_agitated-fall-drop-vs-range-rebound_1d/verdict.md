---
plan: 041-03_agitated-fall-drop-vs-range-rebound_1d
idea: 041-03_agitated-fall-drop-vs-range-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return (vs coin's all-window mean daily return): 0.00363466; t of weighted mean, same-day cases summed: 1.04838 (threshold: confirm: mean > 0 with t >= 2 and positive slope; reject: mean < 0 with t <= -2; min 100 cases on 60 distinct days)
- Supporting check: OLS slope of next-day excess return on forecast: 0.000350324, passed: True
- Counts: cases: 1404, distinct days: 444
- Decided by: t of the weighted mean lies between -2 and 2.
- Reading: Profile bars are those with recorded regime 'unknown' (the config's only active regime); cases are every in-profile bar with forecast > 0 and a next close in the same window; the coin's mean is the mean of all its within-window 1-bar returns; the t uses per-day sums of weighted deviations from the weighted mean (cluster-by-day standard error); the slope is ordinary least squares on all cases; the plan's minimum counts lead to 'not observable' when unmet.
- Size: unusual move +0.15 % (t 0.45, the cases of one day together: 341 days) per case over 1 bars, 0.031 of the coin's usual move (5.40 %); normal drift in its direction +0.15 %, total +0.30 %; 947 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/041-03_agitated-fall-drop-vs-range-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_coins/backtests/041-03_agitated-fall-drop-vs-range-rebound_1d`
Measure: `measure.py`
