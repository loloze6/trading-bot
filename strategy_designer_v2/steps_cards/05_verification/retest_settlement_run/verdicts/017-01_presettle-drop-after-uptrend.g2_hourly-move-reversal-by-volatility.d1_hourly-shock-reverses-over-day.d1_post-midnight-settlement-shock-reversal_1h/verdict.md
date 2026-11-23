---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of drift-adjusted 24-bar return on forecast: 0.000279985; OLS slope t: 8.8578 (threshold: confirm: slope > 0 with t >= 2 (and supporting check > 0); reject: slope < 0 with t <= -2)
- Supporting check: mean sign(forecast) x drift-adjusted 24-bar return, |forecast| >= 10: 0.00457768, passed: True
- Counts: cases pooled over coins and windows: 17048, cases with |forecast| >= 10: 8028
- Decided by: The slope is positive with t >= 2 and the mean signed drift-adjusted return over |forecast| >= 10 is above 0.
- Reading: Cases are the first mean_reversion bar with non-zero forecast per coin per UTC day, the forward return is close 24 rows later in the same window, the drift is the coin's mean 24-bar return on each window's non-overlapping grid pooled over all windows, and the slope is from an OLS with intercept.
- Size: unusual move +0.33 % per case over 24 bars, 0.065 of the coin's usual move (4.87 %); normal drift in its direction +0.00 %, total +0.33 %; 15045 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h`
Measure: `measure.py`
