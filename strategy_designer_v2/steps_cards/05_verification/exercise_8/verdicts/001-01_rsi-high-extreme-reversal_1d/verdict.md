---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess forward 5-bar return after forecast <= -10 vs holding baseline: -0.0119429; t of the mean: -1.32313 (threshold: confirm if negative with t <= -2 (and negative in >= 2 coins); reject if positive with t >= +2; minimum 30 cases)
- Supporting check: number of coins with negative excess return: 2, passed: True
- Counts: non-overlapping extreme cases pooled: 60, coins with negative excess return: 2, coins in record: 2
- Decided by: Inconclusive: the pooled t is strictly between -2 and +2.
- Reading: Extreme cases are grid bars (positions 0,5,10,... of each window) with forecast <= -10, the baseline is the mean forward 5-bar return over all bars of that coin and window with a forward return, the t is the ordinary t of the pooled mean, and the 'at least 2 of the 3 coins' rule is applied as at least 2 negative coins among those present in the record.
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
