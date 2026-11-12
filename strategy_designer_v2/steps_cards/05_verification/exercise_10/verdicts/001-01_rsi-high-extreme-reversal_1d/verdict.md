---
plan: 001-01_rsi-high-extreme-reversal_1d
idea: 001-01_rsi-high-extreme-reversal
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess forward 5-bar return after forecast <= -10 (minus same coin/window mean forward 5-bar return), non-overlapping: -0.0119429; t of the mean: -1.32313 (threshold: confirm: negative with t <= -2 and negative in at least 2 of the 3 coins; reject: positive with t >= +2; inconclusive otherwise or fewer than 30 pooled cases)
- Supporting check: sign of excess return per coin (negative in at least 2 coins): 2, passed: True
- Counts: non-overlapping extreme cases pooled: 60, coins with negative excess return: 2, coins in record: 2, extreme cases BTCUSD: 32, extreme cases ETHUSD: 28
- Decided by: t lies strictly between -2 and +2 (inconclusive rule).
- Reading: Extreme cases are grid bars (positions 0,5,10,... of each window) with forecast <= -10 and a 5-bar forward return inside the window, the baseline is the mean 5-bar forward return over all bars of that coin and window that have one, the t is the ordinary t of the pooled mean, and 'at least 2 of the 3 coins' is applied literally as at least 2 coins with negative mean excess return among the coins present.
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal_1d`
Measure: `measure.py`
