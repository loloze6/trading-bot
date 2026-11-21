---
plan: 016-02_down-grind-price-continuation_1h
idea: 016-02_down-grind-price-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean case gain (forecast/10 x excess 72-bar forward return), non-overlapping grid, forecast < 0: 0.00151387; t of the mean: 0.948179 (threshold: confirm: mean > 0 with t >= 2 (and supporting difference < 0); reject: mean < 0 with t <= -2)
- Supporting check: excess 72-bar return, forecast below median minus above median (Welch t): -4.6098e-05, passed: True
- Counts: grid bars with a negative forecast: 2762, grid bars below median forecast: 1381, grid bars above median forecast: 1381
- Decided by: The main t is between -2 and 2 (inconclusive rule).
- Reading: Grid bars are at positions 0, 72, 144, ... of each window and need an in-window forward return; each coin's mean 72-bar return is taken over all its grid bars in all windows; bars equal to the median forecast are left out of both groups of the supporting check; the plan's 'fewer than 300 grid bars' minimum is treated as 'not observable'.
- Size: unusual move +0.39 % per case over 72 bars, 0.047 of the coin's usual move (8.23 %); normal drift in its direction -0.41 %, total -0.02 %; 4319 cases
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-02_down-grind-price-continuation_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-02_down-grind-price-continuation_1h`
Measure: `measure.py`
