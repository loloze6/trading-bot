---
plan: 002-02_sma-death-cross-downward-drift_1d
idea: 002-02_sma-death-cross-downward-drift
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 20-bar excess log return on forecast at block start: -0.00371536; t of slope, SE clustered by coin: -4.61662 (threshold: slope > 0 with clustered t >= 2 confirms; slope < 0 with t <= -2 rejects)
- Supporting check: share of negative excess blocks when forecast < 0 minus share across all blocks: -0.0625479, passed: False
- Counts: non-overlapping blocks: 811, non-overlapping blocks with forecast below 0: 402
- Decided by: The slope is negative with clustered t <= -2: deeper shorts are followed by rebounds.
- Reading: The situation is the raw component spread (last_history_value) below 0 on the short side; blocks start at positions 0, 20, 40, ... of each window and need close[t+20] inside the window; the coin-window mean is the mean of that coin-window's block log returns; the OLS has an intercept and CR1 standard errors clustered by coin; the supporting check passes when the share for forecast < 0 exceeds the all-block share.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-02_sma-death-cross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-02_sma-death-cross-downward-drift_1d`
Measure: `measure.py`
