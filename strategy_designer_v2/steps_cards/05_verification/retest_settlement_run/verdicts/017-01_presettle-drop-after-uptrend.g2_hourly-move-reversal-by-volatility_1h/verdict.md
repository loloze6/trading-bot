---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-hour excess return on forecast: 1.83357e-05; OLS slope t: 12.2761 (threshold: t >= 2 (with the check) confirms; t <= -2 rejects)
- Supporting check: book mean daily return before costs minus market-rise gain: 0.00185436, passed: True
- Counts: bars of nonzero forecast: 414151, bars in the regression: 416645
- Decided by: The slope's t is at least 2 and the book's mean daily return before costs minus its market gain is above 0.
- Reading: The slope is an OLS with intercept and classic standard errors over all bars (including zero forecasts), the book before costs is rebuilt from the held allocation times the next-hour return compounded per UTC day and averaged over coins, its market gain is the day's mean allocation times the coin's mean daily return, and the plan's 10,000-bar minimum is applied as 'not observable'.
- Size: unusual move +0.01 % per case over 1 bars, 0.014 of the coin's usual move (1.05 %); normal drift in its direction -0.00 %, total +0.01 %; 270123 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h`
Measure: `measure.py`
