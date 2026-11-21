---
plan: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h
idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean 240-bar excess return (return minus normal 240-bar drift) after forecast rises of >= 2 points: 0.00575589; t of the mean: 1.15242 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and positive slope; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: slope of excess return on forecast at signal bar: 0.000890703, passed: True
- Counts: cases: 1148
- Decided by: t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive.
- Reading: The situation is a positive 720-bar close-to-close return (recomputed from prices, the recorded regime used only on the first 720 bars of a window) with a positive raw surge value and a positive forecast; a case is the first bet (forecast rise >= 2 points from its lowest positive level since the last bet, from 0 after a flat) in each 240-bar grid cell counted from each window's first row, and the normal drift is the coin's mean non-overlapping 240-bar return over all its windows.
- Size: unusual move +0.58 % per case over 240 bars, 0.035 of the coin's usual move (14.43 %); normal drift in its direction +1.37 %, total +1.94 %; 1148 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h`
Measure: `measure.py`
