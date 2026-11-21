---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 96-bar move of the cases (return minus the coin's normal 96-bar drift): 0.00702117; t of the mean: 3.38585 (threshold: confirm: mean > 0 with t >= 2 on >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 on >= 30 cases)
- Supporting check: mean unusual move of cases above the median entry forecast minus that of cases below it: None, passed: None
- Counts: cases: 2345
- Decided by: t >= 2 but the supporting check is not above 0.
- Reading: the situation is a positive raw fall-times-rise value (prices used where the raw value is missing); a case is the first bet (forecast rise >= 2 from its lowest level since the last bet, reset at 0) in each 96-bar grid cell from a window's first row, cases without 96 bars left in their window are dropped, and the supporting split uses cases strictly above versus strictly below the median entry forecast.
- Size: unusual move +0.70 % per case over 96 bars, 0.069 of the coin's usual move (8.92 %); normal drift in its direction +0.50 %, total +1.20 %; 2345 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h`
Measure: `measure.py`
