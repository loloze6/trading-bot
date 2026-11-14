---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled excess 5-bar forward return after extreme bars (forecast <= -10) minus own-window drift: -0.0118992; t of the mean: -1.32099 (threshold: confirm if negative with t <= -2 and negative in at least 2 coins; reject if >= 0 or negative in fewer than 2 coins with t > -1; at least 30 pooled and 8 per coin blocks)
- Supporting check: Spearman rank correlation of |forecast| with next 5-bar return over forecast < 0 bars (should be negative): -0.00137397, passed: True
- Counts: pooled non-overlapping extreme blocks: 60, extreme blocks BTCUSD: 32, extreme blocks ETHUSD: 28, coins with negative excess return: 2, coins in record: 2
- Decided by: The pooled excess return is negative with -2 < t <= -1 (or weak with coins split), which meets the inconclusive rule.
- Reading: Extreme bars are non-overlapping grid bars (positions 0,5,10,... per window with a full 5-bar return inside the window) with forecast <= -10, each coin's drift is the mean 5-bar forward return over that window's grid bars, pooled t is the ordinary t of the mean excess, the supporting Spearman correlation uses the same grid bars with forecast < 0, and the 'at least 2 of 3 coins' rule and per-coin minimum apply to the coins present in the record (BTCUSD, ETHUSD; BNB did not run).
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
