---
plan: 031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d
idea: 031-01.b1.b2.b1_wide-day-strong-run-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 3-bar return on positive forecast (day-clustered t): 0.000615843; OLS slope t, clustered by day: 2.49053 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 3-bar return of top third of positive forecasts: 0.0077294, passed: True
- Counts: non-overlapping cases with a forecast above 0: 6115, distinct days: 854
- Decided by: Slope positive with t >= 2 and the top-third mean excess return above 0.
- Reading: Situation taken as raw component > 0 (5-bar return from prices where raw is missing); cases are grid bars 0,3,6,... of each window with forecast > 0 and a 3-bar return inside the window; coin drift is the mean of all its non-overlapping 3-bar grid returns over all windows; slope by OLS with intercept and cluster-robust (by UTC day, CR1) standard error; top third = the floor(n/3) largest positive forecasts; the plan's 'inconclusive' for too few cases is reported as 'not observable'.
- Size: unusual move +0.18 % (t 0.80, the cases of one day together: 1499 days) per case over 3 bars, 0.020 of the coin's usual move (9.14 %); normal drift in its direction +0.47 %, total +0.65 %; 5261 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d`
Measure: `measure.py`
