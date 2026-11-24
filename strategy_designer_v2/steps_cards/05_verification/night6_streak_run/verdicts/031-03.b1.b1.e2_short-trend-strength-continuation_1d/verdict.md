---
plan: 031-03.b1.b1.e2_short-trend-strength-continuation_1d
idea: 031-03.b1.b1.e2_short-trend-strength-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the 5-bar excess return on the forecast, grid bars with forecast > 0, clustered by day: 0.00106411; OLS slope t, errors clustered by day: 1.98209 (threshold: t >= 2 confirms (with the supporting check), t <= -2 rejects, at least 200 grid bars with a positive forecast)
- Supporting check: mean unusual 5-bar move of the cases (forecast rises >= 2 points, once per grid cell), long direction, > 0: -5.28882e-05, passed: False
- Counts: grid bars with a positive forecast: 3587, cases: 3643
- Decided by: The slope's t lies between -2 and 2.
- Reading: The regression uses an intercept and CR1 day-clustered errors on grid bars (positions 0,5,10,... of each window) with post_pipeline_value > 0 and a 5-bar forward return inside the window, the drift is the coin's mean 5-bar grid return over all its windows, the cases are the first forecast rise of at least 2 points per grid cell, and the plan's 'fewer than 200 grid bars' is reported as not observable.
- Size: unusual move -0.01 % (t -0.01, the cases of one day together: 1179 days) per case over 5 bars, 0.004 of the coin's usual move (12.45 %); normal drift in its direction +0.77 %, total +0.76 %; 3643 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.e2_short-trend-strength-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1.b1.e2_short-trend-strength-continuation_1d`
Measure: `measure.py`
