---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of forecast/10 x drift-removed 24-bar return: 0.00221621; t of the mean: 5.02684 (threshold: confirm if t >= 2 (with top third beating bottom third); reject if t <= -2)
- Supporting check: top-third minus bottom-third mean drift-removed return in forecast direction: 0.00158891, passed: True
- Counts: cases with a nonzero forecast: 16838
- Decided by: The main t is 2 or more and the top third beats the bottom third.
- Reading: Cases are grid bars 0,24,48,... of each window with a nonzero forecast and a close 24 bars later in the same window; the coin's mean is over its non-overlapping 24-bar grid returns of all windows; thirds are pooled over all cases by |forecast| (stable sort, numpy array_split); the plan's 'fewer than 500 cases' is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.11 % per case over 24 bars, 0.021 of the coin's usual move (4.87 %); normal drift in its direction +0.00 %, total +0.11 %; 17246 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily_1h`
Measure: `measure.py`
