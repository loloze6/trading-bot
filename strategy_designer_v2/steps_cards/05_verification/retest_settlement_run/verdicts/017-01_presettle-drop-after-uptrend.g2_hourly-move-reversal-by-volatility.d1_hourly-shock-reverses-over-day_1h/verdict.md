---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 24-bar excess forward return on forecast (grid bars, pooled): 4.82659; OLS slope t: 4.82659 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; min 500 grid cases with non-zero forecast)
- Supporting check: none
- Counts: grid cases: 17246, grid cases with a non-zero forecast: 17147
- Decided by: The slope is positive with t = 4.83 >= 2 (confirm rule).
- Reading: The situation is taken as every bar with a non-zero volatility-scaled hourly return (the plan sets no size cut-off, the forecast being graded), the expected side as opposite to that return; the regression is OLS with intercept on all grid bars with valid values, the drift is each coin's mean grid 24-bar return over all its windows, and the plan's minimum of 500 non-zero-forecast grid cases is treated as a minimum count (not observable if unmet).
- Size: unusual move +0.12 % per case over 24 bars, 0.023 of the coin's usual move (4.87 %); normal drift in its direction +0.00 %, total +0.12 %; 17246 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h`
Measure: `measure.py`
