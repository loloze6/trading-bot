---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled 5-bar forward return after extreme (raw>=8) minus after neutral (RSI 40-60) bars: 0.0244546 (threshold: below 0 with t <= -2 to confirm; >= 0 to reject)
- Supporting check: per-coin strategy cumulative return before costs minus same-average-size short hold (min over coins): -0.00840803, passed: False
- Cases: 23
- Decided by: Fewer than 30 pooled non-overlapping extreme cases (23) or fewer than 8 for a coin (min 11) is inconclusive whatever the sign.
- Reading: Neutral RSI is recomputed as Wilder RSI(14) on each window's closes (first bars without RSI dropped), extreme bars use the recorded raw component >= 8, non-overlap is enforced per group per window by taking a case then skipping the next 4 bars, the t is Welch's two-sample t, and with only 2 coins in the record 'negative in at least 2 of 3 coins' requires both coins negative; the supporting check compounds per-bar gains within windows, uses the coin's mean signed allocation as the short size, and passes only if the strategy beats it in every coin.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
