---
plan: 031-01.b1.b1_wide-day-extends-run-more-coins_1d
idea: 031-01.b1.b1_wide-day-extends-run-more-coins
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 3-bar excess forward return on forecast, trending grid bars: 0.00124092; t clustered by day: 2.72679 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: trending grid cases: 9076, distinct days: 1169
- Decided by: Confirm rule: the slope is above 0 with clustered t >= 2.
- Reading: The 5-bar change is recomputed from closes inside each window, so active bars in a window's first 5 rows (no history recorded) are left out of the agreement; trending bars are those with regime == 'trending'; the coin's mean 3-bar return is taken over the 0,3,6,... grid of all its windows; the slope is OLS with intercept of excess return on forecast, with CR1 standard errors clustered by UTC day.
- Size: unusual move +0.28 % (t 1.39, the cases of one day together: 2491 days) per case over 3 bars, 0.025 of the coin's usual move (9.27 %); normal drift in its direction +0.46 %, total +0.73 %; 10129 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.b1_wide-day-extends-run-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/common/backtests/031-01.b1.b1_wide-day-extends-run-more-coins_1d`
Measure: `measure.py`
