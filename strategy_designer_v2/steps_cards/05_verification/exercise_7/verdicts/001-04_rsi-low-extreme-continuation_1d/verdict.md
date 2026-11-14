---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled 5-bar forward return after extreme bars (raw >= 8) minus after neutral bars (RSI 40-60): 0.00927089; Welch t: 0.457902 (threshold: confirm if difference < 0 with Welch t <= -2 and negative in at least 2 coins; reject if difference >= 0)
- Supporting check: per-coin strategy cumulative return before costs minus same-average-size short hold (mean over coins; passes if positive for every coin): 0.492062, passed: True
- Counts: non-overlapping extreme cases pooled: 14, non-overlapping neutral cases pooled: 127, coins with negative difference: 0, extreme cases BTCUSD: 7, extreme cases ETHUSD: 7
- Decided by: Fewer than 30 non-overlapping extreme cases pooled, or fewer than 8 for a coin: inconclusive whatever the sign.
- Reading: Neutral RSI is Wilder RSI(14) recomputed from each window's own closes (first 14 bars of a window have none), the 'at least 2 of the 3 coins' and 'fewer than 8 for any coin' rules are applied to the coins present in the record, and cumulative return is the sum of per-bar position gains across windows.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
