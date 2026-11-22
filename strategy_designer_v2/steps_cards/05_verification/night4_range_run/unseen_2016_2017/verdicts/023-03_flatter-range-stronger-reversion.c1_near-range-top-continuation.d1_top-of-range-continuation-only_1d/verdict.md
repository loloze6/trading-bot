---
plan: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d
idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of 10-day excess return on forecast (non-overlapping grid, forecast > 0): 1.29212; OLS slope t: 1.29212 (threshold: confirm if t >= 2 (with weighted mean excess > 0); reject if t <= -2)
- Supporting check: forecast-weighted mean excess 10-day return: 0.0338707, passed: True
- Counts: grid cells with a forecast above 0: 182
- Decided by: The slope's t lies between -2 and 2.
- Reading: The normal drift is each coin's mean 10-day return over all non-overlapping grid cells of all its windows; the regression pools all coins and windows; the plan's '<100 cells is inconclusive' is applied as the minimum count, giving 'not observable'.
- Size: unusual move +3.07 % per case over 10 bars, 0.090 of the coin's usual move (30.80 %); normal drift in its direction +9.85 %, total +12.92 %; 180 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/unseen_2016_2017/backtests/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d`
Measure: `measure.py`
