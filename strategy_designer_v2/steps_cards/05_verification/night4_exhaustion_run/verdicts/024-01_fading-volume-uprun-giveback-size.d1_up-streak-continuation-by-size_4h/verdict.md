---
plan: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h
idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean of forecast/10 x excess 18-bar return on grid bars with forecast > 0: 0.00287295; t of the mean: 1.20966 (threshold: confirm if t >= 2 (with supporting check), reject if t <= -2)
- Supporting check: top-half minus bottom-half excess 18-bar return, split at median forecast (Welch t): 0.00393732, passed: True
- Counts: grid cases with forecast above 0: 2857, top half cases: 1428, bottom half cases: 1429
- Decided by: The main t lies between -2 and 2.
- Reading: Grid bars are positions 0, 18, 36, ... of each window with the 18-bar return inside the window; drift is the coin's mean 18-bar return on these grids over all windows; the median split puts forecasts above the median in the top half, the rest in the bottom half.
- Size: unusual move -0.09 % per case over 18 bars, -0.009 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.32 %; 5723 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h`
Measure: `measure.py`
