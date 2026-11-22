---
plan: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d
idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of 10-day excess return on forecast (non-overlapping grid, forecast > 0): 0.583853; OLS slope t: 0.583853 (threshold: confirm if t >= 2 (with weighted mean excess > 0); reject if t <= -2)
- Supporting check: forecast-weighted mean excess 10-day return: 0.0328719, passed: True
- Counts: grid cells with a forecast above 0: 81
- Decided by: Only 81 grid cells have a forecast above 0, fewer than the plan's minimum of 100.
- Reading: The normal drift is each coin's mean 10-day return over all non-overlapping grid cells of all its windows; the regression pools all coins and windows; the plan's '<100 cells is inconclusive' is applied as the minimum count, giving 'not observable'.
- Size: unusual move +3.32 % per case over 10 bars, 0.280 of the coin's usual move (9.14 %); normal drift in its direction +0.43 %, total +3.75 %; 100 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/unseen_2026/backtests/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d`
Measure: `measure.py`
