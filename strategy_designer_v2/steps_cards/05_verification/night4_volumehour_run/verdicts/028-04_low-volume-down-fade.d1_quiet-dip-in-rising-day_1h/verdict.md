---
plan: 028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day_1h
idea: 028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 6-bar unusual move of long cases: 0.000554399; t of the mean: 2.22921 (threshold: positive with t >= 2 to confirm, negative with t <= -2 to reject, over at least 30 cases)
- Supporting check: forecast-weighted mean unusual move above 0: 0.000544665, passed: True
- Counts: cases: 5938, active bars: 10433
- Decided by: The mean unusual move is positive with t >= 2 over at least 30 cases and the forecast-weighted mean is above 0.
- Reading: A case is the first bar of each 6-bar grid cell (counted from each window's first row) where the positive forecast rose at least 2 points from its lowest level since the last bet (from 0 after a flat), cases whose 6-bar return would leave the window are dropped, and the drift is the coin's mean 6-bar return on the same grid over all its windows.
- Size: unusual move +0.06 % per case over 6 bars, 0.026 of the coin's usual move (1.98 %); normal drift in its direction +0.03 %, total +0.09 %; 5938 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day_1h`
Measure: `measure.py`
