---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 168-bar strength on forecast, all grid bars: 0.0191782; OLS slope t: 2.43769 (threshold: confirm if t >= 2 (with supporting check), reject if t <= -2)
- Supporting check: mean strength on grid bars with forecast > 0 above 0: 0.0380422, passed: True
- Counts: grid bars: 309, grid bars with forecast > 0: 222
- Decided by: Only 222 grid bars with forecast > 0, fewer than the plan's minimum of 300.
- Reading: The coin's normal drift and usual move are the mean and standard deviation of its forward 168-bar returns on the non-overlapping grid (positions 0, 168, ... of each window) pooled over all its windows, grid bars without a full 168-bar forward return inside the window are dropped, and the plan's '300 grid bars with forecast > 0' is treated as a minimum count giving 'not observable' when not reached.
- Size: unusual move +1.19 % per case over 168 bars, 0.059 of the coin's usual move (22.39 %); normal drift in its direction +7.22 %, total +8.41 %; 239 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/unseen_2016_2017/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h`
Measure: `measure.py`
