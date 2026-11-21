---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-bar excess return on forecast, pooled: 1.83357e-05; OLS slope t: 12.2761 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: bars with a non-zero forecast: 414008, bars in the regression: 416645
- Decided by: The slope is positive with t >= 2 (confirm rule).
- Reading: Every bar with a forecast and a next-bar return inside its window enters the pooled OLS (with intercept), the coin mean is over all its windows' 1-bar returns, and the minimum count is of those bars with a non-zero forecast.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h`
Measure: `measure.py`
