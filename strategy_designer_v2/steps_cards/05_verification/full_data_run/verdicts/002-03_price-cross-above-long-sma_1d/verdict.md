---
plan: 002-03_price-cross-above-long-sma_1d
idea: 002-03_price-cross-above-long-sma
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess forward 10-bar return on positioned blocks vs window mean: -0.0151566; t of the mean: -2.64717 (threshold: mean > 0 with t >= 2 (and hit-rate difference > 0) confirms; mean < 0 with t <= -2 rejects)
- Supporting check: hit rate of positioned blocks minus hit rate of all blocks (slope of forward return on forecast reported in slope_value): -0.00812876, passed: False
- Counts: positioned_blocks_pooled: 816, positioned_blocks_min_per_coin: 112, positioned_blocks_BTCUSD: 157, positioned_blocks_ETHUSD: 159, positioned_blocks_LTCUSD: 120, positioned_blocks_XMRUSD: 146, positioned_blocks_XRPUSD: 122, positioned_blocks_ZECUSD: 112
- Decided by: Rejected: mean excess forward 10-bar return is below 0 with t <= -2.
- Reading: Blocks are the bars at positions 0, 10, 20, ... of each window, and the coin's window mean ("all bars") is taken over that same grid. Positioned means forecast > 0 on the block's first bar. The t is the ordinary t of the pooled mean excess. The per-coin minimum applies to every coin present. The forecast-size slope is reported but not required, because the confirm rule names only the hit-rate difference.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-03_price-cross-above-long-sma_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-03_price-cross-above-long-sma_1d`
Measure: `measure.py`
