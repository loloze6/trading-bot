---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled excess 5-bar forward return after extreme bars (forecast <= -10) minus own window drift: -0.00913528 (threshold: negative with t <= -2 and negative in at least 2 coins to confirm; >= 0 rejects)
- Supporting check: Spearman rank correlation of |forecast| vs next 5-bar return over bars with forecast < 0 (should be negative): 0.0378097, passed: False
- Cases: 80
- Decided by: Pooled excess return is negative with -2 < t = -1.05 <= -1, meeting the inconclusive rule.
- Reading: Only BTC and ETH are in the record, so 'at least 2 of the 3 coins' is read as at least 2 of the coins present, which here means both, and the minimum of 8 blocks applies to each coin present; non-overlapping blocks are taken greedily in time order within each window, keeping an extreme bar and skipping the next 4 bars; drift is the mean 5-bar forward return over all bars in that coin-window; t is the one-sample t of the pooled block excesses; the supporting check uses all bars with forecast < 0 pooled across coins and windows and does not enter the decision.
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
