---
plan: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d
idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 10-bar forward return on forecast (forecast > 0, non-overlapping grid): 0.00556421; OLS slope t: 1.38848 (threshold: confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: mean excess 10-bar return of forecast > 0 grid cases: 0.0153047, passed: True
- Counts: grid cases with forecast > 0: 182, grid cases total: 284
- Decided by: The slope's t lies between -2 and 2.
- Reading: The coin's mean 10-bar return is the mean over all grid cells of all its windows, the slope is an OLS fit with intercept, and the plan's 'fewer than 100 cases' rule is treated as a minimum count giving 'not observable'.
- Size: unusual move +3.20 % per case over 10 bars, 0.082 of the coin's usual move (30.80 %); normal drift in its direction +9.85 %, total +13.06 %; 192 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/unseen_2016_2017/backtests/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d`
Measure: `measure.py`
