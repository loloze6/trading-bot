---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled extreme-minus-neutral 5-bar forward return: 0.00927089; Welch t: 0.457902 (threshold: confirm if below 0 with t <= -2 and negative in at least 2 coins; reject if >= 0; at least 30 extreme cases pooled and 8 per coin)
- Supporting check: strategy cumulative return minus same-average-size short hold, summed over coins: 0.983242, passed: True
- Counts: non-overlapping extreme cases pooled: 14, non-overlapping neutral cases pooled: 127, coins with negative difference: 0, coins in record: 2, extreme cases BTCUSD: 7, neutral cases BTCUSD: 60, extreme cases ETHUSD: 7, neutral cases ETHUSD: 67
- Decided by: Fewer than 30 non-overlapping extreme cases pooled or fewer than 8 for some coin, which is inconclusive whatever the sign.
- Reading: Extreme bars are those with raw component >= 8 and neutral bars are those with Wilder RSI(14) recomputed from each window's own closes between 40 and 60 inclusive (the first 14 bars of each window, with no RSI, are left out of the neutral group); both use the 0,5,10,... grid per window. Since only 2 coins are in the record, 'negative in at least 2 of the 3 coins' is applied literally as at least 2 coins negative. The supporting check uses summed per-bar gains, with the benchmark being a short of the coin's mean absolute allocation, and it passes only if every coin is above zero.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
