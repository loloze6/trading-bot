---
plan: 012-03_lower-wick-flush-recovery_1d
idea: 012-03_lower-wick-flush-recovery
fit: adapted
status: mismatch
---
Situation check: 82 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of the active bars are sharp falls (<= -2 usual moves) on volume at least twice its prior 20-bar mean with a long forecast, so the config does not trade the plan's situation on its side.
- Reading: Situation recomputed from prices as a 1-bar return of -2 or less in units of the std of the last 20 one-bar returns (with or without bar t accepted) and volume at least twice the mean of the prior 20 bars as the Fidelity states, using the recorded regime only on bars with too little in-window history, expected side long; flush bars are regime == mean_reversion with t+3 inside the window, an event at 1 to 3 bars after a kept event is dropped, the coin's mean 3-bar return is taken on the non-overlapping 0,3,6,... grid of all its windows pooled, all flush events (including forecast 0) enter the OLS of excess return on forecast, and the 30-event minimum is on the pooled events of all coins.
Plan: `steps_cards/03_test_plan/volume_run/plans/012-03_lower-wick-flush-recovery_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/012-03_lower-wick-flush-recovery_1d`
Measure: `measure.py`
