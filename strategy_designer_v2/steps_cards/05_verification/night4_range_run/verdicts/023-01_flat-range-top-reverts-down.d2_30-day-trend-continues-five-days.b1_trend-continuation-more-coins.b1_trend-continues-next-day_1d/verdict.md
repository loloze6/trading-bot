---
plan: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast (trending, non-zero forecast bars, pooled): 7.7577e-05; OLS t of slope: 2.61674 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; at least 300 bars)
- Supporting check: none
- Counts: trending bars with a non-zero forecast: 15635
- Decided by: Confirm rule: the slope is positive with t = 2.62 >= 2.
- Reading: Situation computed from prices as |close[t]-close[t-30]| over the 30-bar high-low range (detector's recorded regime used where a window lacks 30 bars of history), side from the sign of the 30-bar return; the plan's 'fewer than 300 bars' minimum is treated as a minimum count (not observable); the coin's mean daily return is the mean of all its in-window next-day returns; OLS with intercept, every bar used since the horizon is 1 bar.
- Size: unusual move +0.07 % per case over 1 bars, 0.008 of the coin's usual move (5.31 %); normal drift in its direction -0.01 %, total +0.07 %; 4366 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d`
Measure: `measure.py`
