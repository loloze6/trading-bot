---
plan: 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d
idea: 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 10-bar excess return on post_pipeline_value (non-overlapping grid, before costs): 0.00551579; OLS slope t, day-clustered: 1.8477 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases in total: 273, grid cases with forecast > 0: 191, days: 82
- Decided by: The plan's minimum count is not reached: 191 grid cases with forecast > 0 (fewer than 200); 273 grid cases in total (fewer than 1000).
- Reading: The coin's mean 10-bar return is the mean of its non-overlapping grid returns over all its windows; 'pooling cases of the same day' is read as a day-clustered standard error for the OLS slope (each day's sum of x-deviation times residual taken as one piece of evidence); grid cases need a forward return inside the window and a recorded post_pipeline_value.
- Size: unusual move +1.11 % (t 0.35, the cases of one day together: 119 days) per case over 10 bars, 0.040 of the coin's usual move (31.94 %); normal drift in its direction +10.05 %, total +11.16 %; 167 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2016_2017/backtests/031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d`
Measure: `measure.py`
