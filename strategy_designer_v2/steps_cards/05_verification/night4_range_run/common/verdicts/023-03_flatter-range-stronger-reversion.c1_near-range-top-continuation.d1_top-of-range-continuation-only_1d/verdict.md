---
plan: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d
idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of 10-day excess return on forecast (non-overlapping grid, forecast > 0): 3.3735; OLS slope t: 3.3735 (threshold: confirm if t >= 2 (with weighted mean excess > 0); reject if t <= -2)
- Supporting check: forecast-weighted mean excess 10-day return: 0.029479, passed: True
- Counts: grid cells with a forecast above 0: 2339
- Decided by: The slope's t is 2 or more and the weighted mean excess return is above 0.
- Reading: The normal drift is each coin's mean 10-day return over all non-overlapping grid cells of all its windows; the regression pools all coins and windows; the plan's '<100 cells is inconclusive' is applied as the minimum count, giving 'not observable'.
- Size: unusual move +1.31 % (t 1.80, the cases of one day together: 1129 days) per case over 10 bars, 0.067 of the coin's usual move (16.74 %); normal drift in its direction +1.49 %, total +2.80 %; 2703 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/common/backtests/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d`
Measure: `measure.py`
