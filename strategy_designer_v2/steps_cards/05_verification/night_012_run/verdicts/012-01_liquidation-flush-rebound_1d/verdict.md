---
plan: 012-01_liquidation-flush-rebound_1d
idea: 012-01_liquidation-flush-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 3-bar excess return after flush bars (vs coin's grid mean): 0.0163073; t of the mean: 2.1102 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases; reject: t <= -2 over >= 30 cases)
- Supporting check: Spearman(forecast, 3-bar excess return) > 0: -0.0094962, passed: False
- Counts: flush cases: 158
- Decided by: Confirming t >= 2 but the Spearman correlation is at or below 0 (supporting check failed).
- Reading: A flush bar is dropped when it lies 1 to 3 bars after any earlier flush bar in the same window (the dedup is applied before dropping cases without a close 3 bars ahead in the window), and the coin's mean is over grid positions 0, 3, 6, ... of each window pooled across all its windows.
Plan: `steps_cards/03_test_plan/night_012_run/plans/012-01_liquidation-flush-rebound_1d.md`
Record: `steps_cards/04_backtest/night_012_run/backtests/012-01_liquidation-flush-rebound_1d`
Measure: `measure.py`
