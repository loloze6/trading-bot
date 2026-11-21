---
plan: 002-03_price-cross-above-long-sma_1d
idea: 002-03_price-cross-above-long-sma
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted 20-bar excess return, block mean over non-overlapping 20-bar blocks (before costs): 0.126305; t of the block mean: 1.72672 (threshold: confirm: block mean > 0 with t >= 2; reject: block mean < 0 with t <= -2; else inconclusive; at least 50 blocks with a non-zero position)
- Supporting check: share of forecast > 0 bars whose next 20-bar return beats 20 x the coin's pooled mean daily return, vs 50%: 0.406015, passed: False
- Counts: non-overlapping 20-bar blocks with a non-zero position: 502, non-overlapping 20-bar blocks: 811, forecast > 0 grid bars (supporting check): 399
- Decided by: The t of the block-mean excess return lies between -2 and 2.
- Reading: The allocation is postRebalance_current_allocation; a block is each run of 20 rows from position 0 of each window and sums allocation x excess over its rows that have a full 20-bar forward return inside the window, all such blocks are pooled for the t (ordinary t of the mean), a block 'has a non-zero position' if any of those rows has a non-zero allocation; the supporting check uses the non-overlapping grid rows (positions 0, 20, 40, ...) with forecast > 0 and passes if the share is above 50%; active rows with a missing raw component value are left out of the situation check.
- Size: unusual move +2.26 % per case over 20 bars, 0.091 of the coin's usual move (21.24 %); normal drift in its direction +2.75 %, total +5.01 %; 367 cases
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-03_price-cross-above-long-sma_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-03_price-cross-above-long-sma_1d`
Measure: `measure.py`
