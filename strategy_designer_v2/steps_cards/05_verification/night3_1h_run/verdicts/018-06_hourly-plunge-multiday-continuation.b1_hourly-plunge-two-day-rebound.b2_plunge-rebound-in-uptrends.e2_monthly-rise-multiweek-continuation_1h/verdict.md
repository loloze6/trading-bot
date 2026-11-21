---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 336-bar return over cells with forecast > 0: 0.024091; t of the forecast-weighted mean over cells: 1.77359 (threshold: confirm: > 0 with t >= 2 (and slope t >= 2); reject: < 0 with t <= -2 or slope t <= -2; at least 200 cells)
- Supporting check: OLS slope of excess return on forecast, t: 2.62226, passed: True
- Counts: cells with forecast > 0: 568
- Decided by: Inconclusive: the main measure's t is between -2 and 2 and no reject rule is met.
- Reading: The t of the weighted mean is the ordinary t of the per-cell values forecast x excess / mean forecast (whose mean equals the weighted mean), the coin's mean 336-bar return is taken on the same non-overlapping grid over all its windows, and the slope's t is the OLS slope over its standard error.
- Size: unusual move +0.75 % per case over 336 bars, 0.029 of the coin's usual move (17.69 %); normal drift in its direction +2.02 %, total +2.77 %; 836 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation_1h`
Measure: `measure.py`
