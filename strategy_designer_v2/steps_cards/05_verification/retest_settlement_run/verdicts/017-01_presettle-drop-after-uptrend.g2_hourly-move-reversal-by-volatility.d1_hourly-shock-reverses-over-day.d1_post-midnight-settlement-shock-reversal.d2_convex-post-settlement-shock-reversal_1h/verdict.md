---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of y = forecast x (r24 - d) over 00:00 bars with |forecast| >= 2: 0.0576208; one-sample t: 8.40849 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: faded return per unit of move, top third minus bottom two thirds: -0.00110551, passed: False
- Counts: cases with |forecast| >= 2: 12716, active bars: 17270, top third cases: 4238, bottom two thirds cases: 8478
- Decided by: t >= 2 but the supporting check failed (top third per unit of move not larger)
- Reading: d is each coin's mean 24-bar return on the non-overlapping grid (positions 0, 24, 48, ... of each window) pooled over all its windows; cases need close[t+24] inside the same window; the raw move is the recorded last_history_value (recomputed from closes where missing); the top third is the floor(n/3) cases with the largest |raw|, the rest are the bottom two thirds; the plan's 'fewer than 100 cases' rule is reported as not observable.
- Size: unusual move +0.37 % per case over 24 bars, 0.072 of the coin's usual move (4.87 %); normal drift in its direction -0.00 %, total +0.37 %; 12677 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal_1h`
Measure: `measure.py`
