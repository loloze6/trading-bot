---
plan: 031-01.b1.b1_wide-day-extends-run-more-coins_1d
idea: 031-01.b1.b1_wide-day-extends-run-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 3-bar excess forward return on forecast, trending grid bars: 0.00114125; t clustered by day: 0.93974 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: trending grid cases: 895, distinct days: 97
- Decided by: Inconclusive rule: the slope's clustered t lies between -2 and 2.
- Reading: The 5-bar change is recomputed from closes inside each window, so active bars in a window's first 5 rows (no history recorded) are left out of the agreement; trending bars are those with regime == 'trending'; the coin's mean 3-bar return is taken over the 0,3,6,... grid of all its windows; the slope is OLS with intercept of excess return on forecast, with CR1 standard errors clustered by UTC day.
- Size: unusual move +0.14 % (t 0.32, the cases of one day together: 228 days) per case over 3 bars, 0.017 of the coin's usual move (6.81 %); normal drift in its direction +0.03 %, total +0.17 %; 1018 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.b1_wide-day-extends-run-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.b1.b1_wide-day-extends-run-more-coins_1d`
Measure: `measure.py`
