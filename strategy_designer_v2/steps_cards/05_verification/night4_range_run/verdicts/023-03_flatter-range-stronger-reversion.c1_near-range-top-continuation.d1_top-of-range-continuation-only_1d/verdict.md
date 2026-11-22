---
plan: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d
idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of 10-day excess return on forecast (non-overlapping grid, forecast > 0): 2.00137; OLS slope t: 2.00137 (threshold: confirm if t >= 2 (with weighted mean excess > 0); reject if t <= -2)
- Supporting check: forecast-weighted mean excess 10-day return: 0.0169243, passed: True
- Counts: grid cells with a forecast above 0: 792
- Decided by: The slope's t is 2 or more and the weighted mean excess return is above 0.
- Reading: The normal drift is each coin's mean 10-day return over all non-overlapping grid cells of all its windows; the regression pools all coins and windows; the plan's '<100 cells is inconclusive' is applied as the minimum count, giving 'not observable'.
- Size: unusual move +0.57 % per case over 10 bars, 0.027 of the coin's usual move (14.49 %); normal drift in its direction +1.16 %, total +1.73 %; 901 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d`
Measure: `measure.py`
