---
plan: 035-01_wide-low-close-rebounds_1d
idea: 035-01_wide-low-close-rebounds
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of next-day excess return on post_pipeline_value: 0.000357586; OLS slope t, day-clustered SE: 3.27302 (threshold: t (day-clustered) >= 2 confirms (with top-fifth mean > 0); t <= -2 rejects)
- Supporting check: mean next-day excess return of the per-coin top fifth of forecast values: 0.00430445, passed: True
- Counts: distinct days with a recorded forecast: 2922, cases: 17380, days with cases: 2898, top-fifth cases: 3479
- Decided by: The slope's t is 2 or more and the top-fifth mean next-day excess return is positive.
- Reading: The slope is an OLS with intercept of next-bar excess return on post_pipeline_value over all coin-bars, its t from a sandwich SE clustered by UTC calendar day (small-sample factor G/(G-1)*(N-1)/(N-2)); 'top fifth' is the bars at or above each coin's 80th percentile of post_pipeline_value; the 500-day minimum counts distinct UTC days with a non-missing post_pipeline_value and, as a minimum count, gives 'not observable'; the situation is a positive raw component value (close below the high) on a long forecast.
- Size: unusual move +0.11 % (t 1.00, the cases of one day together: 2071 days) per case over 1 bars, 0.023 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.23 %; 7102 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001063 on the check folds against +0.0003576 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/035-01_wide-low-close-rebounds_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/035-01_wide-low-close-rebounds_1d`
Measure: `measure.py`
