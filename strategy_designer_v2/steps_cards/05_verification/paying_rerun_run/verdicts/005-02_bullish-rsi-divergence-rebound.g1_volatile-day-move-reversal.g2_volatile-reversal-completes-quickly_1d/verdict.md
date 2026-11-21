---
plan: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed excess 3-bar return on non-overlapping grid bars with |forecast| >= 5: 0.020139; t of the mean: 3.50166 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: t <= -2)
- Supporting check: OLS slope of signed excess 3-bar return on |forecast|, positive with t >= 1: 1.28735, passed: True
- Counts: qualifying cases across all coins and windows: 163
- Decided by: The mean signed excess 3-bar return is above 0 with t >= 2 and the slope on |forecast| is positive with t >= 1.
- Reading: The plan's volatility rule is read from the recorded regime ('mean_reversion' = 20-day vol rank >= 0.8) and a 'large move' bar is any bar with a non-zero one-day move faded by the forecast's sign; the coin's mean 3-bar return is the mean over all non-overlapping grid bars of all its windows; the plan's 'fewer than 30 qualifying cases' is treated as a minimum count giving 'not observable'.
- Size: unusual move +1.37 % per case over 3 bars, 0.201 of the coin's usual move (6.82 %); normal drift in its direction -0.00 %, total +1.36 %; 416 cases
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d`
Measure: `measure.py`
