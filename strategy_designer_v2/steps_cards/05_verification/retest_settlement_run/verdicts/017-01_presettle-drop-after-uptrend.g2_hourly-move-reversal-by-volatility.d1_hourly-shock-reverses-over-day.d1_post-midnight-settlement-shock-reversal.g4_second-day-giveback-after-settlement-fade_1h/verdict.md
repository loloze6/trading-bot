---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade
fit: exact
status: confirmed
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 24-bar forward return minus normal drift on forecast, pooled: 0.000222247; OLS slope t: 5.20299 (threshold: confirm: slope > 0 with t >= 2 (and mean unusual move > 0); reject: slope < 0 with t <= -2; at least 300 cases)
- Supporting check: mean unusual 24-bar move in forecast direction: 0.00241985, passed: True
- Counts: cases: 9041
- Decided by: The slope is positive with t >= 2 and the mean unusual move in the forecast's direction is above 0.
- Reading: The active bar of the situation is the bar stamped 00:00 UTC (closing at 01:00), with r24 the 24-bar return to its close and the hour's move the one-bar return 24 bars earlier, both by row position inside a window; cases are trending bars with non-zero forecast and a full 24-bar forward return in the window, one per day so already non-overlapping, the drift is the coin's mean 24-bar return on the non-overlapping grid of all its windows, the regression is OLS with intercept, and fewer than 300 cases is reported as not observable.
- Size: unusual move +0.27 % per case over 24 bars, 0.057 of the coin's usual move (4.87 %); normal drift in its direction -0.00 %, total +0.27 %; 7904 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade_1h`
Measure: `measure.py`
