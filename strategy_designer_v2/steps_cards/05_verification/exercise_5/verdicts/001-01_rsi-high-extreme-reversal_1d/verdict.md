---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled excess 5-bar forward return after extreme bars (forecast <= -10) minus coin-window drift: -0.0118992; t of the mean: -1.32099 (threshold: negative with t <= -2 and negative in at least 2 of the 3 coins)
- Supporting check: Spearman rank correlation of |forecast| with next 5-bar return, forecast < 0: 0.0378097, passed: False
- Counts: pooled non-overlapping extreme blocks: 60, extreme blocks BTCUSD: 32, extreme blocks ETHUSD: 28, coins with negative excess return: 2, coins in record: 2
- Decided by: Negative pooled excess return with -2 < t <= -1.
- Reading: Drift is the mean 5-bar forward return over the same non-overlapping grid (positions 0,5,10,... per window) as the extreme blocks, the per-coin minimum of 8 and the 'at least 2 coins negative' rule are applied to the coins present in the record (BNB is absent), and the supporting check uses all bars with forecast < 0 pooled across coins and windows.
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
