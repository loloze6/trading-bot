---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 48-bar excess return over coin drift at forecast-rise cases: 0.0018357; t of the mean: 1.9754 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: Spearman(forecast at case, 48-bar excess return) > 0: 0.0274342, passed: True
- Counts: cases: 5958
- Decided by: The t of the mean excess return lies between -2 and 2, which the plan calls inconclusive.
- Reading: A case is a bet bar (forecast rising >= 2 points above its lowest positive level since the last bet, reset to 0 after a flat bar), the first in each 48-bar grid cell counted from the window's first row, kept only when 48 bars remain in the window; the drift is the coin's mean over grid 48-bar returns of all its windows.
- Size: unusual move +0.18 % per case over 48 bars, 0.024 of the coin's usual move (6.56 %); normal drift in its direction +0.27 %, total +0.46 %; 5958 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound_1h`
Measure: `measure.py`
