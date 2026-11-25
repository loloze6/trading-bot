---
plan: 033-01.d1_wide-day-low-close-rebound_1d
idea: 033-01.d1_wide-day-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on post_pipeline_value: 0.000363224; t with cases summed per day (day-clustered OLS t): 3.36232 (threshold: confirm: slope > 0 with day-clustered t >= 2 (and top-fifth mean excess > 0); reject: slope < 0 with t <= -2)
- Supporting check: mean next-day excess return on bars in the per-coin top fifth of forecast: 0.00376634, passed: True
- Counts: bars: 17380, distinct days: 2898, top-fifth bars: 3479
- Decided by: The slope is positive with t >= 2 and the top-fifth mean excess return is above 0.
- Reading: Every bar with a next close in its window and a post_pipeline_value is a case, the coin's mean is its mean 1-bar return over all windows, the t uses OLS score sums per UTC day without small-sample correction, the top fifth is forecast >= the coin's 80th percentile over all its windows, and missing minimum counts give 'not observable' rather than the plan's 'inconclusive'.
- Size: unusual move +0.09 % (t 0.81, the cases of one day together: 2071 days) per case over 1 bars, 0.020 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.21 %; 7074 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001156 on the check folds against +0.0003632 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/033-01.d1_wide-day-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/033-01.d1_wide-day-low-close-rebound_1d`
Measure: `measure.py`
