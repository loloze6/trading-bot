---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 7-bar forward excess return on forecast, regime grid bars: -0.000276332; OLS slope t: -0.373474 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, else inconclusive; at least 100 regime grid cases)
- Supporting check: mean 7-bar excess return of top third by forecast > 0: -0.00125347, passed: False
- Counts: independent regime grid cases: 1226, top third cases: 409
- Decided by: The slope's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: 30-bar return recomputed from closes inside each window (detector's regime used where fewer than 30 prior bars exist); situation = that return < 0 and depth < 0, side long; grid = positions 0,7,14,... of each window with t+7 in the window; coin mean 7-bar return = mean over that coin's grid bars in all windows; top third = regime grid bars with forecast >= its 2/3 quantile.
- Size: unusual move -0.81 % per case over 7 bars, -0.068 of the coin's usual move (12.44 %); normal drift in its direction +0.90 %, total +0.09 %; 927 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends_1d`
Measure: `measure.py`
