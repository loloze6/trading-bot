---
plan: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: one-sample t of mean excess next-day return on bars with forecast >= 5: 0.00245885; one-sample t of the mean: 1.50752 (threshold: confirm if t >= 2 with >= 30 cases and convexity check passes; reject if t <= -2 with >= 30 cases)
- Supporting check: per-unit-forecast mean excess return, group >= 5 minus group 0 < f < 5: -0.000500853, passed: False
- Counts: bars with forecast >= 5: 780, bars with forecast between 0 and 5: 2041
- Decided by: The main t is between -2 and 2.
- Reading: The per-unit-forecast return of each group is taken as the group's mean excess return divided by its mean forecast; 'between 0 and 5' is read as 0 < forecast < 5; every bar is a case, since the 1-bar horizon grid holds every bar; and the coin's mean is that of all its within-window daily returns.
- Size: unusual move +0.06 % per case over 1 bars, 0.014 of the coin's usual move (4.01 %); normal drift in its direction +0.13 %, total +0.18 %; 977 cases
Plan: `steps_cards/03_test_plan/step7ab_bp_run/plans/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d.md`
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d`
Measure: `measure.py`
