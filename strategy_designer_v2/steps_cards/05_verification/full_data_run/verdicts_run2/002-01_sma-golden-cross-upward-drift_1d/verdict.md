---
plan: 002-01_sma-golden-cross-upward-drift_1d
idea: 002-01_sma-golden-cross-upward-drift
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 10-bar forward return minus holding: -0.0225387; t of the forecast-weighted mean excess: -3.2857 (threshold: excess > 0 with t >= 2 to confirm; excess < 0 with t <= -2 to reject)
- Supporting check: hit rate of positive-forecast blocks minus hit rate of all blocks: -0.0201716, passed: False
- Counts: non-overlapping 10-bar blocks with a positive forecast: 832, non-overlapping 10-bar blocks, all: 1657
- Decided by: The excess is negative with t <= -2: reject.
- Reading: Blocks are bars at positions 0,10,20,... of each window for both groups, the holding mean and the all-bar hit rate use that same grid per coin and window, and the t is the forecast-weighted mean of per-block excesses over its weighted (sandwich) standard error across the pooled positive-forecast blocks.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-01_sma-golden-cross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-01_sma-golden-cross-upward-drift_1d`
Measure: `measure.py`
