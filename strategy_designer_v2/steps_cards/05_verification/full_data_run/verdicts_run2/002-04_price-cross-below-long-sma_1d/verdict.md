---
plan: 002-04_price-cross-below-long-sma_1d
idea: 002-04_price-cross-below-long-sma
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of allocation x (10-bar return - 10 x coin mean daily return) over non-overlapping 10-bar blocks, before costs: -0.000724788; t of the mean: -0.274762 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; needs >= 30 nonzero-position blocks)
- Supporting check: OLS slope of excess 10-bar return on allocation, nonzero-position blocks: -0.00561058, passed: False
- Counts: non-overlapping 10-bar blocks with a nonzero position: 930, non-overlapping 10-bar blocks: 1657
- Decided by: The t-statistic lies between -2 and 2: inconclusive.
- Reading: Blocks start at rows 0, 10, 20, ... of each window and need a full 10-bar return inside the window; the pooled mean and t use all such blocks (zero-position blocks contribute zero products) as the plan pools across coins and blocks; the coin's mean daily return is the mean of its within-window close-to-close returns over all its windows.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-04_price-cross-below-long-sma_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-04_price-cross-below-long-sma_1d`
Measure: `measure.py`
