---
plan: 033-01_range-position-drift-follows_1d
idea: 033-01_range-position-drift-follows
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-removed 5-bar forward return on post_pipeline_value, grid cases pooled: 0.000531357; OLS t of slope: 3.17411 (threshold: confirm: slope > 0 with t >= 2 and top-minus-bottom fifth > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean drift-removed 5-bar return, top fifth minus bottom fifth of forecast: 0.0146989, passed: True
- Counts: grid cases across the coins: 3419, top fifth cases: 684, bottom fifth cases: 684
- Decided by: Confirmed on every fold, but the main measure points the other way on the check folds (A, D), the years step 7 does not explore: main measure -0.0001454 on the check folds against +0.0005314 on every fold.
- Reading: Grid = rows 0,5,10,... of each window with close[t+5] in the same window; drift = coin's mean grid 5-bar return over all windows; fifths = pooled 20th/80th percentiles of post_pipeline_value (inclusive); fewer than 500 grid cases is reported as not observable.
- Size: unusual move +0.54 % (t 1.78, the cases of one day together: 1397 days) per case over 5 bars, 0.046 of the coin's usual move (10.60 %); normal drift in its direction -0.02 %, total +0.52 %; 2896 cases
- Direction check on folds A, D (the years step 7 does not explore): disagrees: main measure -0.0001454 on the check folds against +0.0005314 on every fold
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/033-01_range-position-drift-follows_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-01_range-position-drift-follows_1d`
Measure: `measure.py`
