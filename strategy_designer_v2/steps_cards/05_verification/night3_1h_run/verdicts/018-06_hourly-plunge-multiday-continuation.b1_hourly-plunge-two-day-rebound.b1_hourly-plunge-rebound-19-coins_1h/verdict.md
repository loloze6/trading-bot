---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 48-bar move on cases, pooled over coins: 0.00564082; t of the mean: 5.32824 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and positive slope; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: OLS slope of unusual move on forecast at signal bar: 0.001, passed: True
- Counts: cases: 6055
- Decided by: Mean unusual move positive with t >= 2 over at least 30 cases, and the slope on the forecast is positive.
- Reading: A case is the first long bet (forecast rise >= 2 from its lowest level since the last bet, reset to 0 when flat) in each cell of the window's 48-bar grid counted from its first row, with its 48-bar return inside the window; the drift is the coin's mean 48-bar return on that grid over all its windows; the situation is any negative 24-bar return on the long side.
- Size: unusual move +0.56 % per case over 48 bars, 0.071 of the coin's usual move (7.56 %); normal drift in its direction +0.35 %, total +0.92 %; 6055 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h`
Measure: `measure.py`
