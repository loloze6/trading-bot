---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled 5-bar forward return, extreme (raw>=8) minus neutral (RSI 40-60) bars: 0.00927089; Welch t: 0.457902 (threshold: below 0 with t <= -2 and negative in at least 2 of the coins confirms; >= 0 rejects)
- Supporting check: mean over coins of strategy cumulative return minus same-average-size constant position: 0.0550991, passed: False
- Counts: pooled non-overlapping extreme cases: 14, pooled non-overlapping neutral cases: 127, coins: 2, coins with negative difference: 0, extreme cases BTCUSD: 7, extreme cases ETHUSD: 7
- Decided by: Fewer than 30 non-overlapping extreme cases pooled, or fewer than 8 for some coin, is inconclusive whatever the sign.
- Reading: Neutral RSI is Wilder RSI(14) recomputed from each window's closes only (first bars without RSI left out), extremes use the recorded raw component >= 8, both on the 0,5,10,... grid per window; with only 2 coins present 'at least 2 of the 3 coins' requires both coins negative; the supporting check compounds per-bar gains over all windows against a constant position equal to the coin's mean allocation and passes if positive for every coin.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
