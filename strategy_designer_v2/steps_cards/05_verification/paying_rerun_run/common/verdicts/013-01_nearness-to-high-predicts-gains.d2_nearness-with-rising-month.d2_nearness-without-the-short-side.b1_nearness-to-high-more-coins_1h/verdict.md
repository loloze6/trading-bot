---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope t of excess 168-bar forward return on forecast (non-overlapping grid): 0.00187814; OLS slope t: 5.42927 (threshold: confirm if t >= 2 and supporting check passes; reject if t <= -2; else inconclusive; needs >= 300 grid cases with forecast > 0)
- Supporting check: mean excess 168-bar forward return on grid bars with forecast > 0 above 0: 0.00834379, passed: True
- Counts: non-overlapping grid cases with forecast > 0: 2111, non-overlapping grid cases (all): 4241
- Decided by: The slope's t is >= 2 and the mean excess return on forecast > 0 grid bars is above 0.
- Reading: The 720-bar return is recomputed from each window's closes and, on bars without 720 bars of history in the window, its sign is taken from the raw HPM value; the coin's benchmark is the mean of all its non-overlapping 168-bar grid returns over all its windows; the slope's t is the ordinary OLS t with an intercept; the plan's 'fewer than 300 cases' rule is reported as not observable per the workflow.
- Size: unusual move +0.72 % (t 1.72, the cases of one day together: 1241 days) per case over 168 bars, 0.052 of the coin's usual move (14.44 %); normal drift in its direction +1.32 %, total +2.04 %; 2727 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/retest_1h_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h`
Measure: `measure.py`
