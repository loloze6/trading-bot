---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 24-bar return on forecast: 0.000308235; OLS slope t: 9.47881 (threshold: slope > 0 with t >= 2 confirms, slope < 0 with t <= -2 rejects, over at least 1000 cases)
- Supporting check: mean fade gain, high-ratio half minus low-ratio half: 0.00360112, passed: True
- Counts: cases: 17128, cases_with_ratio: 12645, high_ratio_cases: 6322, low_ratio_cases: 6323
- Decided by: Slope positive with t >= 2 over at least 1000 cases and the high-ratio half's fade gain above the low-ratio half's.
- Reading: The situation is the bar whose timestamp (start) is 00:00 UTC with the forecast's sign opposite to the sign of the raw settle_fade value (price return where missing); the slope is an OLS with intercept of excess 24-bar return on forecast; the coin's mean 24-bar return uses the non-overlapping grid 0,24,48,... of each window pooled over its windows; s24 is the ddof-1 std of 24 hourly returns, its 720-bar mean includes bar t, both inside the window, cases without a ratio are left out of the check; the high half is ratio above the median, the low half at or below it.
- Size: unusual move +0.34 % per case over 24 bars, 0.066 of the coin's usual move (4.87 %); normal drift in its direction +0.00 %, total +0.34 %; 14814 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility_1h`
Measure: `measure.py`
