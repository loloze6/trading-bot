---
plan: 002-06_short-below-long-sma-drift-down_1h
idea: 002-06_short-below-long-sma-drift-down
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: t-stat of slope of excess next-24-bar return on forecast (non-overlapping blocks, pooled): 0.649601; OLS slope t: 0.649601 (threshold: confirm if slope t >= 2 with in-zone falling share > 50%; reject if slope t <= -2; at least 60 in-zone blocks)
- Supporting check: in-zone share of blocks with excess 24-bar return < 0 (binomial vs 50%, one-sided p = 0.5615): 0.49734, passed: False
- Counts: in-zone non-overlapping blocks: 376, non-overlapping blocks: 724
- Decided by: Slope t lies between -2 and 2: inconclusive.
- Reading: The window's mean 24-bar return is taken as the mean of that window's non-overlapping grid-block returns (blocks at positions 0, 24, 48, ... with a full 24 bars ahead in the window), the slope t is the OLS slope over its standard error, and the supporting check passes when the share is above 50%.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-06_short-below-long-sma-drift-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-06_short-below-long-sma-drift-down_1h`
Measure: `measure.py`
