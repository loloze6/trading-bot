---
plan: 002-04_price-cross-below-long-sma_1d
idea: 002-04_price-cross-below-long-sma
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean allocation x excess 10-bar return, pooled non-overlapping blocks: -0.000271266; t of the mean: -0.227348 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; otherwise inconclusive)
- Supporting check: slope of excess 10-bar return on allocation, nonzero-position blocks: -0.0125701, passed: False
- Counts: non-overlapping 10-bar blocks with a nonzero position: 931, non-overlapping 10-bar blocks (all): 1657
- Decided by: The t of the mean excess gain lies between -2 and 2 (inconclusive rule).
- Reading: The main measure pools the products of all blocks (zero-position blocks included) as the plan's main measure says, blocks start at rows 0, 10, 20, ... of each window with the allocation after that bar's trade, the coin mean daily return pools all its windows, the situation is below_ma last_history_value < 0 with forecast < 0 (rows with missing values left out), and a block count under 30 is reported as not observable.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-04_price-cross-below-long-sma_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-04_price-cross-below-long-sma_1d`
Measure: `measure.py`
