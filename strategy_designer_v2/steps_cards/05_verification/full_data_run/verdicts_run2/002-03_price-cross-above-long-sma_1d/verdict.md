---
plan: 002-03_price-cross-above-long-sma_1d
idea: 002-03_price-cross-above-long-sma
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted 20-bar excess return per non-overlapping block, before costs: 0.209052; t of the block mean: 1.24871 (threshold: confirm if mean > 0 and t >= 2; reject if mean < 0 and t <= -2; else inconclusive; inconclusive if fewer than 50 blocks with a non-zero position)
- Supporting check: share of forecast>0 bars whose next 20-bar return beats 20 x pooled mean daily return, vs 50%: 0.419813, passed: False
- Counts: non-overlapping 20-bar blocks with a non-zero position: 499, non-overlapping 20-bar blocks: 811, bars with forecast > 0: 7046
- Decided by: The t-statistic lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: Allocation is postRebalance_current_allocation, blocks are bars at positions 0-19, 20-39, ... of each window with bars lacking a 20-bar forward return left out, the t uses all such blocks (zero-position ones included) while the minimum counts blocks holding any non-zero position, and the supporting check passes when the share exceeds 50% over all (overlapping) forecast>0 bars.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-03_price-cross-above-long-sma_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-03_price-cross-above-long-sma_1d`
Measure: `measure.py`
