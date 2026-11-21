---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 168-bar move of grid bars with forecast > 0 (return minus coin's mean 168-bar return): 0.00733568; t of the mean: 1.27323 (threshold: confirm: mean > 0 with t >= 2 over >= 100 independent cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: mean unusual move of upper half minus lower half, split at median forecast: 0.0297041, passed: True
- Counts: independent cases: 750, upper half cases: 375, lower half cases: 375
- Decided by: The t-statistic lies between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are pooled over all coins, each coin's drift is the mean 168-bar return over its grid bars in all windows, the upper half is forecast strictly above the median (ties go to the lower half), and the year condition is read from the recorded 'trending' regime.
- Size: unusual move +0.88 % per case over 168 bars, 0.062 of the coin's usual move (12.47 %); normal drift in its direction +1.02 %, total +1.90 %; 960 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years_1h`
Measure: `measure.py`
