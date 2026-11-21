---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 168-bar move after bets (return minus coin's normal 168-bar drift): -0.000851811; t of the mean: -0.278137 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and slope > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: slope of unusual move on forecast at signal bar: 0.000528865, passed: True
- Counts: cases: 1883
- Decided by: The t-statistic of the mean unusual move lies between -2 and 2.
- Reading: A bet is a rise of the positive forecast of at least 2 points from its lowest level since the last bet (reset to 0 when the forecast is not positive and at each window's start), the first bet of each 168-bar grid cell counted from the window's first row is the case, cases without 168 bars ahead in their window are dropped, and the normal drift is the coin's mean non-overlapping 168-bar return over all its windows.
- Size: unusual move -0.09 % per case over 168 bars, -0.005 of the coin's usual move (12.47 %); normal drift in its direction +0.99 %, total +0.91 %; 1883 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising_1h`
Measure: `measure.py`
