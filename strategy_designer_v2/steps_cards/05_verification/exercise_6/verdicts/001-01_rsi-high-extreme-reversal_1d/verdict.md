---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled excess 5-bar forward return after extreme bars (forecast <= -10) minus own window drift: -0.0118992; t of the mean: -1.32099 (threshold: confirm if negative with t <= -2 and negative in >= 2 of the coins; reject if >= 0 or negative in < 2 coins with t > -1)
- Supporting check: Spearman rank correlation of |forecast| vs next 5-bar return, bars with forecast < 0 (should be negative): 0.0378097, passed: False
- Counts: pooled non-overlapping extreme blocks: 60, coins with negative excess return: 2, extreme blocks BTCUSD: 32, extreme blocks ETHUSD: 28
- Decided by: Negative pooled excess return with -2 < t <= -1 (or split coins without t > -1).
- Reading: Extreme blocks are grid bars at positions 0,5,10,... of each window with forecast <= -10, drift is the mean 5-bar forward return over that same grid in the window, t is the ordinary t of the pooled excess mean, the '2 of 3 coins' rule and the 8-per-coin minimum are applied to the coins present in the record (BTCUSD, ETHUSD), and the supporting rank correlation uses all bars with forecast < 0 (not only the grid).
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
