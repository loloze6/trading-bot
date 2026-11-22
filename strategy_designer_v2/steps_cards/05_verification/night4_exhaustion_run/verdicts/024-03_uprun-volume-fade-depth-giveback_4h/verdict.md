---
plan: 024-03_uprun-volume-fade-depth-giveback_4h
idea: 024-03_uprun-volume-fade-depth-giveback
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move in the short direction over the short bets: 0.00127935; t of the mean: 1.1475 (threshold: mean > 0 with t >= 2 over at least 30 cases to confirm; t <= -2 over at least 30 cases to reject)
- Supporting check: high-fade minus low-fade mean unusual fall (median split of vol_fade raw): 0.001523, passed: True
- Counts: cases: 5709, high-fade cases: 1200, low-fade cases: 4509
- Decided by: The t of the mean unusual fall lies between -2 and 2.
- Reading: The situation is a bar inside a current up-streak (the bar closed above the previous close, or run_gain's raw value is positive) with a short forecast; a case is the first short bet (forecast falling at least 2 points below its highest level on the short side since its last bet, from 0 after a flat or a side change) in each 18-bar grid cell of a window, with a full 18-bar return inside the window; the drift is the coin's mean 18-bar return on the grid of all its windows; the high-fade half is cases with vol_fade raw value above the median and the low-fade half those at or below it.
- Size: unusual move +0.13 % per case over 18 bars, 0.014 of the coin's usual move (8.17 %); normal drift in its direction -0.41 %, total -0.28 %; 5709 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-03_uprun-volume-fade-depth-giveback_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-03_uprun-volume-fade-depth-giveback_4h`
Measure: `measure.py`
