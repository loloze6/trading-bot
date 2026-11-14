---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled 5-bar forward return, extreme (raw>=8) minus neutral (RSI 40-60) bars: 0.00927089; Welch t: 0.457902 (threshold: below 0 with t <= -2 and negative in at least 2 of the 3 coins to confirm; >= 0 rejects)
- Supporting check: mean per-coin cumulative strategy return minus same-average-size constant short (passed if > 0 for every coin): 0.0550991, passed: False
- Counts: pooled non-overlapping extreme cases: 14, pooled non-overlapping neutral cases: 127, coins: 2, coins with negative difference: 0, BTCUSD non-overlapping extreme cases: 7, ETHUSD non-overlapping extreme cases: 7
- Decided by: Fewer than 30 non-overlapping extreme cases pooled, or fewer than 8 for a coin, is inconclusive whatever the sign.
- Reading: Extreme bars use the recorded raw component >= 8 and neutral bars use Wilder RSI(14) recomputed from each window's closes (40 <= RSI <= 60, rows without enough history skipped), both on the 0,5,10,... grid per window; with only the coins present, 'at least 2 of the 3 coins' is applied literally as at least 2 negative coins with none positive, minimum counts are checked first, then a non-negative pooled difference rejects; the supporting check compounds per-bar gains within windows per coin against a constant position equal to the coin's mean allocation.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
