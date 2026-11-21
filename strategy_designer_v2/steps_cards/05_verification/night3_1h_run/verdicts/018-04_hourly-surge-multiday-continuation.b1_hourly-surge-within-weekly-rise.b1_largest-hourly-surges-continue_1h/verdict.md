---
plan: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue_1h
idea: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 120-bar excess return over the coin's normal drift, per bet case: 0.00116173; t of the mean: 0.518562 (threshold: mean > 0 with t >= 2 and >= 30 cases (confirm); mean < 0 with t <= -2 and >= 30 cases (reject))
- Supporting check: mean excess (forecast >= 10) minus mean excess (forecast < 10), Welch: 0.00903116, passed: True
- Counts: cases: 2455, cases_forecast_ge_10: 677, cases_forecast_lt_10: 1778
- Decided by: The t of the mean lies between -2 and 2, which the plan calls inconclusive.
- Reading: A case is the first bet (forecast rise >= 2 from its long-side low since the last bet) in each 120-bar grid cell counted from the window's first row, its forecast is the forecast at that bar, the drift is the coin's mean non-overlapping 120-bar return over all its windows, and the supporting check passes when the difference of means is above 0 (the Welch t is reported, not thresholded).
- Size: unusual move +0.12 % per case over 120 bars, 0.007 of the coin's usual move (10.37 %); normal drift in its direction +0.64 %, total +0.76 %; 2455 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue_1h`
Measure: `measure.py`
