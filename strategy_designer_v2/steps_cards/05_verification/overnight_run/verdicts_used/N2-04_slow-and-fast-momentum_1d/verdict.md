---
plan: N2-04_slow-and-fast-momentum_1d
idea: N2-04_slow-and-fast-momentum
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 20-bar forward excess return (vs coin mean 20-bar return) on active bars, non-overlapping, pooled: 0.0183228; t of the mean: 0.817797 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; inconclusive otherwise or if fewer than 30 non-overlapping active blocks)
- Supporting check: OLS slope of 20-bar excess return on forecast level (active, non-overlapping): 0.00400197, passed: True
- Counts: non-overlapping 20-bar active blocks: 269
- Decided by: The t-statistic of the mean 20-bar excess return lies between -2 and 2 (inconclusive rule).
- Reading: The coin's mean 20-bar return is the mean of every bar's 20-bar forward return across all of that coin's windows (all bars, overlapping), and active blocks are bars with forecast > 0 on the grid 0, 20, 40, ... of each window with a complete 20-bar forward return inside the window; the t-statistic is mean / (sd / sqrt(n)) and the supporting slope is the OLS slope of excess return on forecast over those same blocks.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N2-04_slow-and-fast-momentum_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N2-04_slow-and-fast-momentum_1d`
Measure: `measure.py`
