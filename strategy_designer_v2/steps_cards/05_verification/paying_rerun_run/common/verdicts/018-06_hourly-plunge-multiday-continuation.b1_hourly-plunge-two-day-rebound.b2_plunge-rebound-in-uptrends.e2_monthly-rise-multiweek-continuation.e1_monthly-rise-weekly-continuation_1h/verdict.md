---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 168-bar strength on forecast, all grid bars: 0.0121551; OLS slope t: 5.8995 (threshold: confirm if t >= 2 (with supporting check), reject if t <= -2)
- Supporting check: mean strength on grid bars with forecast > 0 above 0: 0.0652128, passed: True
- Counts: grid bars: 4849, grid bars with forecast > 0: 2418
- Decided by: The slope's t is 2 or more and the mean strength on forecast > 0 grid bars is above 0.
- Reading: The coin's normal drift and usual move are the mean and standard deviation of its forward 168-bar returns on the non-overlapping grid (positions 0, 168, ... of each window) pooled over all its windows, grid bars without a full 168-bar forward return inside the window are dropped, and the plan's '300 grid bars with forecast > 0' is treated as a minimum count giving 'not observable' when not reached.
- Size: unusual move +1.04 % (t 2.00, the cases of one day together: 1311 days) per case over 168 bars, 0.063 of the coin's usual move (14.92 %); normal drift in its direction +1.62 %, total +2.66 %; 2983 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h`
Measure: `measure.py`
