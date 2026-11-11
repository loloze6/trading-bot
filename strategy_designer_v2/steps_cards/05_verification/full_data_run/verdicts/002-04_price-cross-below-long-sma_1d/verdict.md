---
plan: 002-04_price-cross-below-long-sma_1d
idea: 002-04_price-cross-below-long-sma
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of allocation x (10-bar return - 10 x coin mean daily return), non-overlapping blocks, pooled: -0.000724788; t of the mean: -0.274762 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; needs >= 30 nonzero-position blocks)
- Supporting check: slope of excess 10-bar return on allocation, nonzero-position blocks: -0.00561058, passed: False
- Counts: non-overlapping 10-bar blocks with a nonzero position: 930, non-overlapping 10-bar blocks: 1657, active bars: 8748
- Decided by: The t-statistic lies between -2 and 2, so the result is inconclusive.
- Reading: The mean and its t are taken over all pooled blocks, zero-position blocks included, because the main measure pools the products across all coins and blocks. Blocks start at positions 0, 10, 20, ... of each window and need the close 10 bars later in the same window. The coin's mean daily return pools the within-window daily returns of all its windows.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-04_price-cross-below-long-sma_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-04_price-cross-below-long-sma_1d`
Measure: `measure.py`
