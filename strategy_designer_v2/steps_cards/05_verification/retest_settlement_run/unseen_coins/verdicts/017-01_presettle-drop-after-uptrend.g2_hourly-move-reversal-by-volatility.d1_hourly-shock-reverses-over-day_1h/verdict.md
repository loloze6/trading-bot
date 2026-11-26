---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 24-bar excess forward return on forecast (grid bars, pooled): 3.02426; OLS slope t: 3.02426 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; min 500 grid cases with non-zero forecast)
- Supporting check: none
- Counts: grid cases: 19406, grid cases with a non-zero forecast: 19263
- Decided by: The slope is positive with t = 3.02 >= 2 (confirm rule).
- Reading: The situation is taken as every bar with a non-zero volatility-scaled hourly return (the plan sets no size cut-off, the forecast being graded), the expected side as opposite to that return; the regression is OLS with intercept on all grid bars with valid values, the drift is each coin's mean grid 24-bar return over all its windows, and the plan's minimum of 500 non-zero-forecast grid cases is treated as a minimum count (not observable if unmet).
- Size: unusual move +0.14 % (t 2.02, the cases of one day together: 2529 days) per case over 24 bars, 0.025 of the coin's usual move (5.73 %); normal drift in its direction -0.00 %, total +0.14 %; 19405 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +3.893 on the check folds against +3.024 on every fold
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/unseen_coins/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h`
Measure: `measure.py`
