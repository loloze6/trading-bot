---
plan: 020-04_support-breakdown-continues-down_1d
idea: 020-04_support-breakdown-continues-down
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean unusual 5-bar move of short cases, pooled: 0.00196303; t of the mean: 0.731839 (threshold: t >= 2 (with check) confirms, t <= -2 rejects, between is inconclusive; at least 30 cases)
- Supporting check: mean unusual move, larger-|forecast| half minus smaller half: -0.000413901, passed: False
- Counts: cases pooled across coins: 1536, larger half: 768, smaller half: 768
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: A case is the first short bet (forecast deepening >= 2 points from its least-deep short level since the last bet, reset at flat) in each 5-bar grid cell from each window's first row, with its 5-bar return inside the window; drift is the coin's mean 5-bar return on that grid over all its windows; the larger half is |forecast| strictly above the median, the rest the smaller half; the situation is a non-zero raw component value and the side is forecast < 0.
- Size: unusual move +0.20 % per case over 5 bars, 0.017 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total -0.39 %; 1536 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-04_support-breakdown-continues-down_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-04_support-breakdown-continues-down_1d`
Measure: `measure.py`
