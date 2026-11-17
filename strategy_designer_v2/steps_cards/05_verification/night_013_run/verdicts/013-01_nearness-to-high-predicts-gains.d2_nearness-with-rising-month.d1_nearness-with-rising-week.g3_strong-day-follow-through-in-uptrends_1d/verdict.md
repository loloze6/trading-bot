---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 7-bar excess forward return on forecast, trending grid bars: 0.00110197; OLS slope t: 3.01294 (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; at least 100 grid cases)
- Supporting check: none
- Counts: trending grid cases: 1215
- Decided by: The slope is positive with t >= 2 on at least 100 grid cases (the confirm rule).
- Reading: The coin's mean 7-bar return is taken over all non-overlapping grid bars of all its windows, whatever their regime. 'Trending' grid bars are read from the recorded regime column. In the situation check, the 30-bar return is recomputed from prices, falling back to the recorded regime on the first 30 bars of a window. The expected side there is the sign of the raw zday value, or of the 1-bar return where zday is not recorded.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends_1d`
Measure: `measure.py`
