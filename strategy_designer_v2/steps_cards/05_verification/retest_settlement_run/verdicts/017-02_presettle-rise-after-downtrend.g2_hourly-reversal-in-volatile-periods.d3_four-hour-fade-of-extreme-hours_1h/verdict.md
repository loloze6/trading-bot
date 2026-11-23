---
plan: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours_1h
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 4-bar return on forecast: 5.88556e-05; OLS slope t: 9.3816 (threshold: slope > 0 with t >= 2 confirms (with supporting check); slope < 0 with t <= -2 rejects)
- Supporting check: mean of sign(forecast) x excess 4-bar return over top fifth of |forecast|: 0.00131254, passed: True
- Counts: non-overlapping sampled bars with a non-zero forecast: 103416, sampled bars: 104088, top-fifth sampled bars: 20818
- Decided by: The slope is positive with t >= 2 and the top-fifth mean of sign(forecast) x excess return is above 0.
- Reading: Active bars for the situation check are those with a non-zero forecast and a recorded raw value; the regression uses all sampled bars (zero forecasts included) with an intercept and the classic OLS standard error; the coin's mean 4-bar return is the mean of its sampled returns over all its windows; the top fifth is the sampled bars with |forecast| at or above the 80th percentile of |forecast| over all sampled bars.
- Size: unusual move +0.03 % per case over 4 bars, 0.016 of the coin's usual move (2.03 %); normal drift in its direction -0.00 %, total +0.03 %; 100163 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours_1h`
Measure: `measure.py`
