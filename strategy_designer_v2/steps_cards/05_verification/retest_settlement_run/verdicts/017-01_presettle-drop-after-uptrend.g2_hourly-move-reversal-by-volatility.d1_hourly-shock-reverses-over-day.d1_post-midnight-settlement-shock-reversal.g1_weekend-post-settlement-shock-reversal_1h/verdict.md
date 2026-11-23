---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the 24-bar excess return on the recorded forecast, weekend 00:00 cases: 0.000367709; OLS slope t: 7.37206 (threshold: confirm: slope > 0 with t >= 2 over >= 1000 weekend cases and weekend slope > weekday slope; reject: slope < 0 with t <= -2 over >= 1000 cases)
- Supporting check: weekend slope minus weekday slope (> 0): 0.000133277, passed: True
- Counts: weekend cases: 4912, weekday cases: 12217
- Decided by: Weekend slope positive with t >= 2 over at least 1000 weekend cases and the weekend slope exceeds the weekday slope.
- Reading: Cases are all Saturday/Sunday (weekend) and Monday-Friday (weekday) bars stamped 00:00 UTC with a 24-bar forward return inside their window (forecast 0 included), the coin mean is over its non-overlapping 24-bar grid of all windows, and the weekday forecast is rebuilt as return/rolling 24-bar std (ddof 1, current bar included), standardised over the previous 60 bars' raw values on every bar (min 20), negated and clipped to +-20.
- Size: unusual move +0.41 % per case over 24 bars, 0.082 of the coin's usual move (4.87 %); normal drift in its direction -0.01 %, total +0.41 %; 4279 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal_1h`
Measure: `measure.py`
