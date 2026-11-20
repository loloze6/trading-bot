---
plan: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound_1d
idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-bar return on forecast, pooled: 0.000859739; OLS slope t: 2.2238 (threshold: confirm if slope t >= 2 with supporting check passing; reject if slope t <= -2)
- Supporting check: top-third minus bottom-third forecast mean excess 3-bar return > 0: 0.00923223, passed: True
- Counts: independent grid cases in the falling regime: 2815
- Decided by: The slope's t is at least 2 and the top-minus-bottom-third excess return is above 0.
- Reading: Cases are the bars at positions 0,3,6,... of each window with regime mean_reversion, a recorded forecast and a close 3 bars later in the same window (zero forecasts kept); the coin's mean 3-bar return is taken over the same grid on all its bars in all windows; top and bottom thirds are the n//3 highest and lowest forecasts by stable sort.
- Size: unusual move -0.13 % per case over 3 bars, -0.014 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.23 %; 2493 cases
Plan: `steps_cards/03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound_1d.md`
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound_1d`
Measure: `measure.py`
