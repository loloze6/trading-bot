---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled 5-bar forward return after extreme (raw >= 8) minus after neutral (RSI 40-60) bars: 0.0244546 (threshold: below 0 with t <= -2 to confirm; >= 0 rejects)
- Supporting check: per-coin cumulative strategy return minus constant short of same average size (mean over coins): 0.0550991, passed: False
- Cases: 23
- Decided by: Fewer than 30 non-overlapping extreme cases pooled, or fewer than 8 for a coin, is inconclusive whatever the sign.
- Reading: Neutral RSI is a Wilder RSI(14) recomputed within each window, with bounds 40 and 60 inclusive. Non-overlapping cases are taken greedily per window and group, skipping 4 bars after each case. t is a Welch two-sample t. Only 2 coins are in the record, so 'at least 2 of 3 coins negative' requires both to be negative. For the supporting check: the average size is the signed mean allocation, returns are compounded within each window and chained across windows, and the check passes if every coin's excess is > 0.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
