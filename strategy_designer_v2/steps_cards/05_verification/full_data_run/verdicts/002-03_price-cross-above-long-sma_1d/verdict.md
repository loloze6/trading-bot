---
plan: 002-03_price-cross-above-long-sma_1d
idea: 002-03_price-cross-above-long-sma
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted 20-bar excess return, block mean over non-overlapping 20-bar blocks: 0.339761; t of the block mean: 1.24898 (threshold: confirm if block mean > 0 with t >= 2; reject if block mean < 0 with t <= -2; else inconclusive; inconclusive if fewer than 50 blocks with a non-zero position)
- Supporting check: share of forecast>0 bars whose next 20-bar return beats 20 x pooled mean daily return, vs 50%: 0.419813, passed: False
- Counts: non-overlapping 20-bar blocks with a non-zero position: 499, non-overlapping 20-bar blocks: 811, bars with forecast > 0: 7046
- Decided by: Inconclusive: t lies between -2 and 2.
- Reading: Allocation is postRebalance_current_allocation, blocks are rows 0-19, 20-39, ... of each window summed over bars that have a 20-bar forward return, the t-statistic is taken over the blocks holding a non-zero position (the blocks the plan's minimum counts), and the supporting check passes when the share exceeds 50%.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-03_price-cross-above-long-sma_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-03_price-cross-above-long-sma_1d`
Measure: `measure.py`
