---
plan: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 336-bar forward return minus coin drift on forecast (grid bars with forecast > 0): 0.00378061; OLS slope t: 2.5172 (threshold: confirm if slope t >= 2 (with top-tercile mean excess > 0 and >= 100 cases); reject if t <= -2 (>= 100 cases))
- Supporting check: top-tercile (by forecast) mean 336-bar excess return over drift > 0: 0.0341754, passed: True
- Counts: grid cases with forecast > 0: 559, top tercile cases: 187
- Decided by: Slope t is 2 or more, the top-tercile mean excess return is above 0, with at least 100 cases.
- Reading: The regression pools all coins' grid bars with forecast > 0 (grid from each window's first row, returns inside the window), the drift is each coin's mean 336-bar return over all its windows' grid bars, and the top tercile is the top third of those bars ranked by forecast (ties broken by order).
- Size: unusual move +1.20 % per case over 336 bars, 0.048 of the coin's usual move (17.69 %); normal drift in its direction +2.22 %, total +3.42 %; 824 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h`
Measure: `measure.py`
