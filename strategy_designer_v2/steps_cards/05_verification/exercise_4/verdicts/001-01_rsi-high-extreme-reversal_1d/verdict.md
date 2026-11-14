---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled 5-bar excess forward return after extreme bars (forecast <= -10) minus coin-window drift: -0.0118992; one-sample t of the mean: -1.32099 (threshold: confirm if negative with t <= -2 and negative in at least 2 coins; reject if >= 0 or negative in fewer than 2 coins with t > -1)
- Supporting check: Spearman rank correlation of |forecast| with next 5-bar return over bars with forecast < 0: 0.0378097, passed: False
- Counts: pooled non-overlapping extreme blocks: 60, extreme blocks BTCUSD: 32, extreme blocks ETHUSD: 28, coins with negative excess return: 2
- Decided by: A negative pooled excess return with -2 < t <= -1 (or otherwise between rules), which is inconclusive.
- Reading: Drift is each window's mean 5-bar forward return over the same non-overlapping grid (positions 0,5,10,... from the window's first row), the 'at least 2 of the 3 coins' and 'at least 8 per coin' rules are applied to the coins present in the record (BTCUSD, ETHUSD; BNB is absent) with the threshold of 2 kept, and the supporting check uses all in-window bars with forecast < 0 and is reported but does not enter the decision.
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
