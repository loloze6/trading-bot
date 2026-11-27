---
plan: 024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues_4h
idea: 024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of OLS slope of excess 18-bar return on forecast (non-overlapping grid, pooled): 7.96778; OLS slope t: 7.96778 (threshold: confirm if t >= +2 (and positive-forecast cells' mean excess > 0); reject if t <= -2)
- Supporting check: mean excess 18-bar return of grid cells with forecast > 0: 0.00525342, passed: True
- Counts: grid cells: 11111, grid cells with forecast > 0: 5426
- Decided by: The slope's t is +2 or more and the positive-forecast cells' mean excess return is above 0.
- Reading: Grid cells are rows 0, 18, 36, ... of each window with the forecast at the cell's bar; the coin's mean 18-bar return is the mean over its grid cells pooled across all its windows; the plan's 'fewer than 200 positive cells' is reported as not observable.
- Size: unusual move +0.49 % (t 2.22, the cases of one day together: 1849 days) per case over 18 bars, 0.050 of the coin's usual move (9.37 %); normal drift in its direction +0.70 %, total +1.19 %; 4891 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/common/backtests/024-03_uprun-volume-fade-depth-giveback.d2_stretch-above-average-continues_4h`
Measure: `measure.py`
