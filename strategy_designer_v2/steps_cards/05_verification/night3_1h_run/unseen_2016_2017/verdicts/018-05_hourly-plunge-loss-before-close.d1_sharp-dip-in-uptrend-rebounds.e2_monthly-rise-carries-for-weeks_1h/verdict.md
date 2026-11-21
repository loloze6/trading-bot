---
plan: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 336-bar forward return minus coin drift on forecast (grid bars with forecast > 0): 0.00109527; OLS slope t: 0.13266 (threshold: confirm if slope t >= 2 (with top-tercile mean excess > 0 and >= 100 cases); reject if t <= -2 (>= 100 cases))
- Supporting check: top-tercile (by forecast) mean 336-bar excess return over drift > 0: -0.0223563, passed: False
- Counts: grid cases with forecast > 0: 43, top tercile cases: 15
- Decided by: Only 43 grid cases with forecast > 0, fewer than the plan's minimum of 100.
- Reading: The regression pools all coins' grid bars with forecast > 0 (grid from each window's first row, returns inside the window), the drift is each coin's mean 336-bar return over all its windows' grid bars, and the top tercile is the top third of those bars ranked by forecast (ties broken by order).
- Size: unusual move -0.86 % per case over 336 bars, -0.068 of the coin's usual move (30.14 %); normal drift in its direction +12.08 %, total +11.22 %; 51 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/unseen_2016_2017/backtests/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h`
Measure: `measure.py`
