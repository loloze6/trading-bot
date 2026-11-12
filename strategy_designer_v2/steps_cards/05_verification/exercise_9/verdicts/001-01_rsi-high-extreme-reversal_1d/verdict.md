---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess forward 5-bar return after forecast <= -10 (vs coin-window mean): -0.0119429; t of the mean: -1.32313 (threshold: confirm: excess < 0 with t <= -2 and negative in at least 2 of 3 coins; reject: excess > 0 with t >= +2; minimum 30 non-overlapping extreme cases)
- Supporting check: number of coins with negative mean excess return (need >= 2): 2, passed: True
- Counts: pooled non-overlapping extreme cases: 60, coins with negative excess: 2, coins in record: 2, extreme cases BTCUSD: 32, extreme cases ETHUSD: 28
- Decided by: t lies strictly between -2 and +2 (inconclusive rule).
- Reading: Extreme cases are grid bars (positions 0,5,10,... per window) with forecast <= -10 and a defined in-window 5-bar forward return, the baseline is the mean forward 5-bar return over all bars of that coin-window that have one, and with BNB absent the 'at least 2 of the 3 coins' rule is applied literally as at least 2 negative coins among those present.
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
