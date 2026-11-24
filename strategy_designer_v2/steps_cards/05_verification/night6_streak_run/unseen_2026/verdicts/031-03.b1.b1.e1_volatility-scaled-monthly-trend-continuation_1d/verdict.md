---
plan: 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d
idea: 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 10-bar excess return on post_pipeline_value (non-overlapping grid, before costs): 0.00284902; OLS slope t, day-clustered: 1.28747 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases in total: 570, grid cases with forecast > 0: 283, days: 30
- Decided by: The plan's minimum count is not reached: 570 grid cases in total (fewer than 1000).
- Reading: The coin's mean 10-bar return is the mean of its non-overlapping grid returns over all its windows; 'pooling cases of the same day' is read as a day-clustered standard error for the OLS slope (each day's sum of x-deviation times residual taken as one piece of evidence); grid cases need a forward return inside the window and a recorded post_pipeline_value.
- Size: unusual move +1.02 % (t 0.72, the cases of one day together: 102 days) per case over 10 bars, 0.097 of the coin's usual move (11.10 %); normal drift in its direction +0.34 %, total +1.36 %; 333 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2026/backtests/031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d`
Measure: `measure.py`
