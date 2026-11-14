---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled excess 5-bar forward return after extreme bars (forecast <= -10), minus coin-window drift: -0.0119429 (threshold: negative with t <= -2 to confirm; >= 0 rejects; -2 < t <= -1 is inconclusive)
- Supporting check: Spearman rank correlation of |forecast| with next 5-bar return, forecast < 0: 0.0378097, passed: False
- Cases: 60
- Decided by: The pooled excess return is negative with -2 < t <= -1 (or otherwise between the confirm and reject rules), which meets the inconclusive rule. (t = -1.323130383155041, per-coin mean excess = {'BTCUSD': -0.013672559612544174, 'ETHUSD': -0.00996604522921871}, per-coin blocks = {'BTCUSD': 32, 'ETHUSD': 28})
- Reading: Non-overlapping blocks are a fixed 5-bar grid from each window's first bar, and a block counts as extreme when its start bar has forecast <= -10. Drift is the mean of all valid 5-bar forward returns in that coin-window. t is the one-sample t of the pooled block excess returns. 'At least 2 of the 3 coins' and the 8-per-coin minimum are applied to the coins present in the record. The supporting check uses every bar with forecast < 0 and a valid 5-bar forward return, pooled across coins and windows.
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
