---
plan: 031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d
idea: 031-01.b1.b2.b1_wide-day-strong-run-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 3-bar return on positive forecast (day-clustered t): 0.000629078; OLS slope t, clustered by day: 2.67958 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 3-bar return of top third of positive forecasts: 0.0101483, passed: True
- Counts: non-overlapping cases with a forecast above 0: 9076, distinct days: 1169
- Decided by: Slope positive with t >= 2 and the top-third mean excess return above 0.
- Reading: Situation taken as raw component > 0 (5-bar return from prices where raw is missing); cases are grid bars 0,3,6,... of each window with forecast > 0 and a 3-bar return inside the window; coin drift is the mean of all its non-overlapping 3-bar grid returns over all windows; slope by OLS with intercept and cluster-robust (by UTC day, CR1) standard error; top third = the floor(n/3) largest positive forecasts; the plan's 'inconclusive' for too few cases is reported as 'not observable'.
- Size: unusual move +0.16 % (t 0.73, the cases of one day together: 2045 days) per case over 3 bars, 0.016 of the coin's usual move (9.27 %); normal drift in its direction +0.45 %, total +0.61 %; 7788 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/common/backtests/031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d`
Measure: `measure.py`
