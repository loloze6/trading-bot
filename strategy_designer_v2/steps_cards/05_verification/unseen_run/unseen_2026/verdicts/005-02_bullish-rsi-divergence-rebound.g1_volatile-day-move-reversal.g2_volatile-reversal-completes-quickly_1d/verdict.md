---
plan: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed excess 3-bar return on non-overlapping grid bars with |forecast| >= 5: -0.018958; t of the mean: -1.9132 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: t <= -2)
- Supporting check: OLS slope of signed excess 3-bar return on |forecast|, positive with t >= 1: -1.53443, passed: False
- Counts: qualifying cases across all coins and windows: 15
- Decided by: Only 15 qualifying cases (grid bars with |forecast| >= 5), below the plan's minimum of 30.
- Reading: The plan's volatility rule is read from the recorded regime ('mean_reversion' = 20-day vol rank >= 0.8) and a 'large move' bar is any bar with a non-zero one-day move faded by the forecast's sign; the coin's mean 3-bar return is the mean over all non-overlapping grid bars of all its windows; the plan's 'fewer than 30 qualifying cases' is treated as a minimum count giving 'not observable'.
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d.md`
Record: `steps_cards/04_backtest/unseen_run/unseen_2026/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d`
Measure: `measure.py`
