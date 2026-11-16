---
plan: 002-06_short-below-long-sma-drift-down_1h
idea: 002-06_short-below-long-sma-drift-down
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t-stat of slope of next-24-bar excess return on forecast at block start: 0.649601; OLS slope t: 0.649601 (threshold: Confirm if slope t >= 2 with in-zone falling share > 50%; reject if slope t <= -2; at least 60 in-zone blocks)
- Supporting check: in-zone share of blocks with excess 24-bar return < 0 (binomial vs 50%, two-sided p=0.9589): 0.49734, passed: False
- Counts: in-zone non-overlapping blocks: 376, non-overlapping blocks: 724
- Decided by: Slope t is between -2 and 2, so the result is inconclusive.
- Reading: Blocks start at positions 0, 24, 48, ... of each window. Each window's drift is the mean of its own non-overlapping block returns. The slope t is from OLS with an intercept on all pooled blocks. In-zone means forecast < 0. The supporting check passes on a share above 50%, and the binomial test is two-sided and reported only.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-06_short-below-long-sma-drift-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-06_short-below-long-sma-drift-down_1h`
Measure: `measure.py`
