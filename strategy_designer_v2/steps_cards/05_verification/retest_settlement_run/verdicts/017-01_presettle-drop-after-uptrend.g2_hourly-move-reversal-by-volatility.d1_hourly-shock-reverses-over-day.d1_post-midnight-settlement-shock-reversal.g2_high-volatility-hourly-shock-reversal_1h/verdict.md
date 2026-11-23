---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 24-bar return on forecast (grid cases, pooled): 0.000377509; OLS slope t: 5.16014 (threshold: confirm: slope > 0 with t >= 2 and support passes; reject: slope < 0 with t <= -2; else inconclusive; minimum 300 grid cases)
- Supporting check: mean of excess return x sign(forecast) > 0: 0.00353963, passed: True
- Counts: grid cases: 5403
- Decided by: The slope is positive with t >= 2 and the mean signed excess return is above 0.
- Reading: Situation bars use the 24/720-bar return-std ratio recomputed from in-window closes (falling back to the recorded regime where fewer than 720 prior returns exist) and the expected side is minus the sign of the raw fade value; the coin's mean 24-bar return is taken over all grid bars of all its windows; the plan's 'fewer than 300 grid cases' minimum is reported as 'not observable'.
- Size: unusual move +0.07 % per case over 24 bars, 0.013 of the coin's usual move (4.87 %); normal drift in its direction +0.00 %, total +0.07 %; 8563 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h`
Measure: `measure.py`
