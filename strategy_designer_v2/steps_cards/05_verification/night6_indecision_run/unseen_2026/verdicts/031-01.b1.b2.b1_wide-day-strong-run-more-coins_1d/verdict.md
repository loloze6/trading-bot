---
plan: 031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d
idea: 031-01.b1.b2.b1_wide-day-strong-run-more-coins
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 3-bar return on positive forecast (day-clustered t): 0.000648603; OLS slope t, clustered by day: 0.988513 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 3-bar return of top third of positive forecasts: 0.00877806, passed: True
- Counts: non-overlapping cases with a forecast above 0: 895, distinct days: 97
- Decided by: Minimum counts not reached: 895 cases (need 300) on 97 days (need 150).
- Reading: Situation taken as raw component > 0 (5-bar return from prices where raw is missing); cases are grid bars 0,3,6,... of each window with forecast > 0 and a 3-bar return inside the window; coin drift is the mean of all its non-overlapping 3-bar grid returns over all windows; slope by OLS with intercept and cluster-robust (by UTC day, CR1) standard error; top third = the floor(n/3) largest positive forecasts; the plan's 'inconclusive' for too few cases is reported as 'not observable'.
- Size: unusual move +0.22 % (t 0.42, the cases of one day together: 201 days) per case over 3 bars, 0.045 of the coin's usual move (6.81 %); normal drift in its direction +0.04 %, total +0.25 %; 788 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d`
Measure: `measure.py`
