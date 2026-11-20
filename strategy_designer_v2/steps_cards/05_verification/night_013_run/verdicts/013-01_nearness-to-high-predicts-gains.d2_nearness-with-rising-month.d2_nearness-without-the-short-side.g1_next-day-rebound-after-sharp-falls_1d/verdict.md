---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of OLS slope of next-day excess return on forecast, forecast>0 bars: 0.00032777; OLS slope t: 3.90392 (threshold: confirm if slope t >= 2 with mean timing gain > 0; reject if slope t <= -2; at least 500 bars with forecast > 0)
- Supporting check: mean daily timing gain of the book (position x (coin return - coin mean)): 0.000541129, passed: True
- Counts: bars with forecast > 0: 8514, book days: 2898
- Decided by: Slope t is 2 or more and the mean timing gain is above 0, meeting the confirm rule.
- Reading: The 500-bar minimum counts forecast > 0 bars that have a next-day close in the same window, and the daily book's timing gain is each day's mean over coins of postRebalance_current_allocation x (next-day return - coin mean), averaged over all days.
- Size: unusual move +0.19 % per case over 1 bars, 0.039 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.31 %; 5665 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls_1d`
Measure: `measure.py`
