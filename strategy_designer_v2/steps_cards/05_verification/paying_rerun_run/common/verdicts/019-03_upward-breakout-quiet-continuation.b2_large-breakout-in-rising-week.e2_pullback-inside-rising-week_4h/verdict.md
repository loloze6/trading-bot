---
plan: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 18-bar excess return on forecast (pooled, grid bars with forecast > 0): 0.00120583; OLS slope t: 5.14334 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, at least 100 cases)
- Supporting check: mean of forecast x excess return > 0: 0.0663001, passed: True
- Counts: independent grid cases with forecast > 0: 4984
- Decided by: The slope's t is 2 or more, the supporting check passes, with at least 100 cases.
- Reading: The 42-bar return is close[t]/close[t-42]-1 inside the window, with the recorded regime used on the first 42 bars of a window where prices cannot give it; the pullback depth is the recorded raw value, recomputed from prices where missing; the coin's normal drift is the mean 18-bar return over all grid bars of all its windows; the slope's t is the ordinary OLS t of the pooled regression of excess return on forecast with an intercept, and a case is a grid bar with forecast > 0 and a full 18-bar forward return.
- Size: unusual move +0.20 % (t 0.99, the cases of one day together: 2099 days) per case over 18 bars, 0.020 of the coin's usual move (9.37 %); normal drift in its direction +0.71 %, total +0.91 %; 7917 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h`
Measure: `measure.py`
