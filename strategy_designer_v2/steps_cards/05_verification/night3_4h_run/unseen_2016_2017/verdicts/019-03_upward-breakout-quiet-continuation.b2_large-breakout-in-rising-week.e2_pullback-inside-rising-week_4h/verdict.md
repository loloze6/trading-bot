---
plan: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 18-bar excess return on forecast (pooled, grid bars with forecast > 0): -0.00025163; OLS slope t: -0.281791 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, at least 100 cases)
- Supporting check: mean of forecast x excess return > 0: 0.00841214, passed: True
- Counts: independent grid cases with forecast > 0: 466
- Decided by: The slope's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The 42-bar return is close[t]/close[t-42]-1 inside the window, with the recorded regime used on the first 42 bars of a window where prices cannot give it; the pullback depth is the recorded raw value, recomputed from prices where missing; the coin's normal drift is the mean 18-bar return over all grid bars of all its windows; the slope's t is the ordinary OLS t of the pooled regression of excess return on forecast with an intercept, and a case is a grid bar with forecast > 0 and a full 18-bar forward return.
- Size: unusual move +0.34 % per case over 18 bars, 0.026 of the coin's usual move (13.56 %); normal drift in its direction +3.06 %, total +3.40 %; 706 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/unseen_2016_2017/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h`
Measure: `measure.py`
