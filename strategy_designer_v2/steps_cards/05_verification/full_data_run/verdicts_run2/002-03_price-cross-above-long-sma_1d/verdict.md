---
plan: 002-03_price-cross-above-long-sma_1d
idea: 002-03_price-cross-above-long-sma
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess forward 10-bar return on positioned non-overlapping blocks (vs coin's window mean over all bars): -0.0163522; one-sample t of the mean excess: -2.85507 (threshold: confirm: mean > 0 with t >= 2 and hit-rate difference > 0; reject: mean < 0 with t <= -2; inconclusive otherwise or if < 100 positioned blocks pooled or < 10 per coin)
- Supporting check: hit-rate difference (positioned blocks minus all blocks); slope of forward return on forecast reported: -0.00812876, passed: False
- Counts: positioned blocks pooled: 816, positioned blocks BTCUSD: 157, positioned blocks ETHUSD: 159, positioned blocks LTCUSD: 120, positioned blocks XMRUSD: 146, positioned blocks XRPUSD: 122, positioned blocks ZECUSD: 112
- Decided by: The mean excess forward return is below 0 with t <= -2.
- Reading: Blocks are the bars at positions 0, 10, 20, ... of each window with forecast > 0; the coin's mean is taken over every bar of the window with a valid forward return; the hit rate across all blocks uses the same grid; the slope is reported but only the hit-rate difference enters the confirm rule, as the plan writes; the per-coin minimum applies to every coin present in the record.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-03_price-cross-above-long-sma_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-03_price-cross-above-long-sma_1d`
Measure: `measure.py`
