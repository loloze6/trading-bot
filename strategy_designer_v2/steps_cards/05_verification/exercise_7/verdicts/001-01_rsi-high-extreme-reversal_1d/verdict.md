---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess 5-bar forward return after extreme bars (forecast <= -10) minus coin's window drift: -0.0118992; t of the mean: -1.32099 (threshold: confirm: pooled excess < 0 with t <= -2 and negative in >= 2 coins; reject: pooled excess >= 0, or negative in < 2 coins with t > -1; min 30 pooled non-overlapping extreme blocks and 8 per coin)
- Supporting check: Spearman rank correlation of |forecast| with next 5-bar return, bars with forecast < 0: 0.0378097, passed: False
- Counts: pooled_non_overlapping_extreme_blocks: 60, extreme_blocks_BTCUSD: 32, extreme_blocks_ETHUSD: 28, coins_with_negative_excess: 2
- Decided by: The pooled excess return is negative with -2 < t <= -1.
- Reading: The coin's drift is the mean 5-bar forward return over the same non-overlapping grid (positions 0, 5, 10, ...) of each window, the per-coin sign is the mean excess over that coin's extreme blocks, the 'at least 2 of the 3 coins' rule is applied as at least 2 negative coins among the coins present, and the supporting correlation uses all bars with forecast < 0.
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
