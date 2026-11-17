---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess next-1-bar return on forecast: 0.000396759; t of OLS slope: 3.10704 (threshold: confirm: slope > 0 with t >= 2 and weighted mean excess > 0; reject: slope < 0 with t <= -2; else inconclusive; at least 100 qualifying bars)
- Supporting check: forecast-weighted mean excess next-1-bar return: 0.00305766, passed: True
- Counts: qualifying bars: 3839
- Decided by: The slope is positive with t >= 2 and the forecast-weighted mean excess return is above 0.
- Reading: The plan's situation is taken as the 30-day close-to-close return > 0 (from prices inside the window, the recorded regime where 30 prior bars are missing) and a negative raw vol-scaled 1-day return (the recorded 'fall' value, else the 1-day price return), side long; the coin's mean daily return is the mean of all its next-1-bar returns over all windows; the slope t is the OLS slope over its standard error.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d`
Measure: `measure.py`
