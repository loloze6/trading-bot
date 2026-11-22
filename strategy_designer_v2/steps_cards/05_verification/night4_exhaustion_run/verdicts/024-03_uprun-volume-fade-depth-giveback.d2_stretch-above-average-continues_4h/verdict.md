---
plan: 024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues_4h
idea: 024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of OLS slope of excess 18-bar return on forecast (non-overlapping grid, pooled): 4.62449; OLS slope t: 4.62449 (threshold: confirm if t >= +2 (and positive-forecast cells' mean excess > 0); reject if t <= -2)
- Supporting check: mean excess 18-bar return of grid cells with forecast > 0: 0.00388312, passed: True
- Counts: grid cells: 5724, grid cells with forecast > 0: 2748
- Decided by: The slope's t is +2 or more and the positive-forecast cells' mean excess return is above 0.
- Reading: Grid cells are rows 0, 18, 36, ... of each window with the forecast at the cell's bar; the coin's mean 18-bar return is the mean over its grid cells pooled across all its windows; the plan's 'fewer than 200 positive cells' is reported as not observable.
- Size: unusual move +0.44 % per case over 18 bars, 0.049 of the coin's usual move (8.17 %); normal drift in its direction +0.40 %, total +0.83 %; 2516 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues_4h`
Measure: `measure.py`
