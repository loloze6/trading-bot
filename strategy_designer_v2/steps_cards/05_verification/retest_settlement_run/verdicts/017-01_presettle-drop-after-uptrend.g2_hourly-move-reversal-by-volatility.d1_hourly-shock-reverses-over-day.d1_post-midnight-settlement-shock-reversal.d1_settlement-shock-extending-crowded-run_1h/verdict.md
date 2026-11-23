---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
fit: adapted
status: confirmed
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 24-bar forward return on forecast: 0.000363776; OLS slope t: 7.87247 (threshold: slope > 0 with t >= 2 (confirm), slope < 0 with t <= -2 (reject), on at least 300 cases)
- Supporting check: mean of sign(forecast) x excess 24-bar return > 0: 0.00452308, passed: True
- Counts: cases: 8162
- Decided by: The slope is positive with t >= 2 on at least 300 cases and the supporting check passes.
- Reading: Situation bars are those stamped 00:00 UTC whose own return close[t]/close[t-1]-1 has the same sign as close[t-1]/close[t-24]-1, expected side opposite to that hour's return; a coin-day's case is its first non-zero-forecast bar (UTC date of the timestamp); the coin's mean 24-bar return is taken on the non-overlapping 24-bar grid of all its windows; the slope is ordinary least squares with an intercept and t = slope / its standard error.
- Size: unusual move +0.49 % per case over 24 bars, 0.096 of the coin's usual move (4.87 %); normal drift in its direction -0.00 %, total +0.49 %; 7172 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h`
Measure: `measure.py`
