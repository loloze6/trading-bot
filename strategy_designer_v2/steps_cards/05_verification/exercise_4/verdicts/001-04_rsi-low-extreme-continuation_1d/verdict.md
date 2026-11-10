---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled 5-bar forward return, extreme (component>=8) minus neutral (RSI 40-60): 0.00927089; Welch t: 0.457902 (threshold: confirm if below 0 with t <= -2 and negative in at least 2 of the 3 coins; reject if >= 0)
- Supporting check: mean per-coin cumulative strategy return minus same-average-size short hold (passed if positive for every coin): 0.0550991, passed: False
- Counts: non-overlapping extreme cases pooled: 14, non-overlapping neutral cases pooled: 127, coins with negative difference: 0, coins with positive difference: 2, coins in record: 2, extreme cases BTCUSD: 7, neutral cases BTCUSD: 60, difference BTCUSD: 0.0169073, extreme cases ETHUSD: 7, neutral cases ETHUSD: 67, difference ETHUSD: 0.00141941, strategy minus same-size short BTCUSD: 0.118606, strategy minus same-size short ETHUSD: -0.00840803
- Decided by: Fewer than 30 pooled non-overlapping extreme cases or fewer than 8 for some coin, which is inconclusive whatever the sign.
- Reading: Extreme bars use the recorded component >= 8 while neutral bars use Wilder RSI(14) recomputed from each window's closes (40 <= RSI <= 60, extreme bars excluded), both sampled on the 0,5,10,... grid per window; with only 2 coins in the record 'negative in at least 2 of the 3 coins' requires both to be negative; the supporting check compounds per-bar gains within windows against a short of the mean absolute allocation and passes only if positive for every coin.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
