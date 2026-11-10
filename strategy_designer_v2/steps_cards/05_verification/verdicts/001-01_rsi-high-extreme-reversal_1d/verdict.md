---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess forward 5-bar return after forecast <= -10 (vs holding baseline): -0.0119429; t of the mean: -1.32313 (threshold: confirm if negative with t <= -2; reject if positive with t >= +2; at least 30 cases)
- Supporting check: number of coins with negative mean excess return: 2, passed: True
- Counts: non-overlapping extreme cases pooled: 60, coins: 2, coins with negative excess: 2
- Decided by: The pooled t lies strictly between -2 and +2, meeting the inconclusive rule.
- Reading: The holding baseline is the mean forward 5-bar return over all bars of each coin and window (not only grid bars), extreme cases are grid bars at positions 0,5,10,... with forecast <= -10, and 'at least 2 of the 3 coins' is applied literally as at least 2 coins negative, which with only BTC and ETH in the record means both.
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
