---
plan: 031-01.b1_near-yearly-low-falls-all-coins_1d
idea: 031-01.b1_near-yearly-low-falls-all-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of the 20-bar excess forward return on the forecast (non-overlapping grid): 0.00158173; date-clustered OLS t of the slope: 1.07358 (threshold: confirm: slope > 0 with t >= 2 and top-quintile check passed; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 20-bar return of the top quintile of |forecast| below 0: -0.0325744, passed: True
- Counts: grid cases: 1495, distinct dates: 147, top-quintile cases: 299
- Decided by: Inconclusive rule: the slope's |t| is below 2.
- Reading: Grid = rows 0, 20, 40, ... of each window with the forward return inside the window; excess = return minus the coin's mean grid 20-bar return over all its windows; all grid cases with a forecast are used (zero forecasts included); OLS with intercept, t from date-clustered standard errors (cases of one date pooled, G/(G-1) correction); top quintile = cases with |forecast| at or above its 80th percentile.
- Size: unusual move -1.56 % (t -0.93, the cases of one day together: 343 days) per case over 20 bars, -0.064 of the coin's usual move (23.14 %); normal drift in its direction -2.99 %, total -4.55 %; 740 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.b1_near-yearly-low-falls-all-coins_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.b1_near-yearly-low-falls-all-coins_1d`
Measure: `measure.py`
