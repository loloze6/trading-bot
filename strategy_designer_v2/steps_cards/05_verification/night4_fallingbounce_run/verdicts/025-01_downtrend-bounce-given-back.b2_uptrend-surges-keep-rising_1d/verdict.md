---
plan: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d
idea: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 5-bar forward return on forecast, cells with forecast > 0, coins pooled: 0.00211576; OLS slope t: 3.81532 (threshold: confirm if t >= 2 (with the supporting check), reject if t <= -2, at least 30 cells with forecast above 0)
- Supporting check: mean excess 5-bar return on cells with forecast >= 5 above 0: 0.0242782, passed: True
- Counts: grid cells with forecast above 0: 909, grid cells with forecast 5 or more: 283
- Decided by: The slope's t is 2 or more and the mean excess 5-bar return on cells with forecast 5 or more is above 0, with at least 30 cells.
- Reading: The 90-day return is recomputed from closes inside each window where 90 prior bars exist, otherwise the recorded regime 'trending' (the detector's ret90 >= 0 decision) is used; the up-day is last_history_value > 0; the coin's mean 5-bar return is the mean over all grid cells of all its windows; the slope and t come from ordinary least squares of excess return on forecast over all pooled cells with forecast > 0; with no cell at forecast 5 or more the supporting check counts as failed.
- Size: unusual move +0.37 % per case over 5 bars, 0.030 of the coin's usual move (10.60 %); normal drift in its direction +0.58 %, total +0.95 %; 1283 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d`
Measure: `measure.py`
