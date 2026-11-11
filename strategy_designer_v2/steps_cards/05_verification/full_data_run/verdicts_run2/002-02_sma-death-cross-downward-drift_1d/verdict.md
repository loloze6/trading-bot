---
plan: 002-02_sma-death-cross-downward-drift_1d
idea: 002-02_sma-death-cross-downward-drift
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 20-bar excess log return on forecast (non-overlapping blocks): -0.00371536; OLS slope t, SE clustered by coin (CR1): -4.61662 (threshold: confirm if slope > 0 with coin-clustered t >= 2; reject if slope < 0 with t <= -2; else inconclusive; at least 100 blocks with forecast < 0)
- Supporting check: share of negative excess blocks when forecast < 0 minus share across all blocks: -0.0625479, passed: False
- Counts: non-overlapping blocks with forecast below 0: 402, non-overlapping blocks: 811, coins: 6
- Decided by: The slope is negative with coin-clustered t <= -2: deeper shorts are followed by rebounds.
- Reading: Blocks start at rows 0, 20, 40, ... of each window with the full 20-bar forward log return inside the window; the coin-window mean 20-bar return is the mean of those block returns; the regression is pooled OLS with intercept and Stata-style CR1 coin-clustered standard errors; the supporting check passes if the short-block share of negative excess returns exceeds the all-block share.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-02_sma-death-cross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-02_sma-death-cross-downward-drift_1d`
Measure: `measure.py`
