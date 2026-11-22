---
plan: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d
idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move in the short direction: -0.00767388; t of the mean: -1.85497 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases)
- Supporting check: stronger-half minus weaker-half mean unusual move: -0.000442468, passed: False
- Counts: cases: 895, stronger half: 448, weaker half: 447
- Decided by: t between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are the bars at positions 0, 5, 10, ... of each window with a 5-bar return inside the window and forecast <= -2; the drift is the coin's mean 5-bar return on that grid over all its windows; the stronger half is the cases with forecast at or below the median forecast, the weaker half those above it.
- Size: unusual move -0.21 % per case over 5 bars, -0.020 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total -0.79 %; 1138 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d`
Measure: `measure.py`
