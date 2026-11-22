---
plan: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-excess 5-bar return on forecast, non-overlapping grid, pooled: 0.000544798; OLS slope t: 4.13041 (threshold: slope t >= 2 (confirm, with timing gain > 0) or <= -2 (reject), on >= 300 grid cases with non-zero forecast)
- Supporting check: timing gain (mean daily gain before costs minus market-rise gain): 0.000898404, passed: True
- Counts: grid cases with a non-zero forecast: 7267, grid cases: 7270
- Decided by: The slope's t is 2 or more on at least 300 grid cases with a non-zero forecast, and the timing gain is above 0.
- Reading: The regression uses every grid case of each window (bars 0, 5, 10, ... from its first row), including those with a zero forecast, with an intercept, and the drift is each coin's mean of those grid returns over all its windows; the timing gain uses the position held after each bar times the next bar's coin return, with the market part being that position times the coin's mean daily return over all its windows, both averaged over coins each day and then over days.
- Size: unusual move +0.75 % per case over 5 bars, 0.051 of the coin's usual move (12.35 %); normal drift in its direction -0.04 %, total +0.72 %; 5233 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d`
Measure: `measure.py`
