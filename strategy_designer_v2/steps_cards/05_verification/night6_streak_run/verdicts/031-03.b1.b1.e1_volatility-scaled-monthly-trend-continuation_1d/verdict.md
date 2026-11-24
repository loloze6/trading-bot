---
plan: 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d
idea: 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 10-bar excess return on post_pipeline_value (non-overlapping grid, before costs): 0.00188198; OLS slope t, day-clustered: 2.34309 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases in total: 3551, grid cases with forecast > 0: 1723, days: 304
- Decided by: The slope is positive with t = 2.34 >= 2 (plan's confirm rule; no supporting check).
- Reading: The coin's mean 10-bar return is the mean of its non-overlapping grid returns over all its windows; 'pooling cases of the same day' is read as a day-clustered standard error for the OLS slope (each day's sum of x-deviation times residual taken as one piece of evidence); grid cases need a forward return inside the window and a recorded post_pipeline_value.
- Size: unusual move +1.55 % (t 2.03, the cases of one day together: 732 days) per case over 10 bars, 0.085 of the coin's usual move (16.61 %); normal drift in its direction +1.43 %, total +2.99 %; 1763 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d`
Measure: `measure.py`
