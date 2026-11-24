---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 24-bar excess forward return on forecast (grid bars, pooled): -0.523608; OLS slope t: -0.523608 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; min 500 grid cases with non-zero forecast)
- Supporting check: none
- Counts: grid cases: 1908, grid cases with a non-zero forecast: 1896
- Decided by: The slope's t = -0.52 lies strictly between -2 and 2 (inconclusive rule).
- Reading: The situation is taken as every bar with a non-zero volatility-scaled hourly return (the plan sets no size cut-off, the forecast being graded), the expected side as opposite to that return; the regression is OLS with intercept on all grid bars with valid values, the drift is each coin's mean grid 24-bar return over all its windows, and the plan's minimum of 500 non-zero-forecast grid cases is treated as a minimum count (not observable if unmet).
- Size: unusual move -0.08 % (t -0.61, the cases of one day together: 318 days) per case over 24 bars, -0.022 of the coin's usual move (3.25 %); normal drift in its direction -0.00 %, total -0.08 %; 1908 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/unseen_2026/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h`
Measure: `measure.py`
