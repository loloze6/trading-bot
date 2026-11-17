---
plan: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of Monday excess return on Sunday forecast: 0.000338419; OLS slope t: 3.16373 (threshold: confirm: slope > 0 with t >= 2 and volume difference > 0 with t >= 2; reject: slope < 0 with t <= -2 or difference < 0 with t <= -2)
- Supporting check: high-volume minus low-volume slope, t: -0.0001205, passed: False
- Counts: Sunday cases: 2489, high-volume half: 1242, low-volume half: 1247
- Decided by: the result meets neither the confirm rule nor the reject rule, so it is inconclusive
- Reading: Sunday cases are the regime 'mean_reversion' bars with a next bar in the same window, the slope is OLS with intercept on the 'forecast' column, the volume split is per coin at the median of sunday_volume last_history_value over all its Sunday cases (high = above median, low = at or below), the difference t is (b_high - b_low)/sqrt(se_high^2 + se_low^2), and the situation side is taken from the sign of sunday_move last_history_value (price return if missing).
Plan: `steps_cards/03_test_plan/volume_run/plans/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d`
Measure: `measure.py`
