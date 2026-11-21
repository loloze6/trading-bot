---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume
fit: exact
status: confirmed
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 7-day excess return on forecast: 0.00244546; OLS slope t: 4.17064 (threshold: slope t >= 2 confirms (with timing gain > 0); slope t <= -2 rejects)
- Supporting check: timing gain (book mean daily return before costs minus market-rise gain): 0.000330727, passed: True
- Counts: non-overlapping samples: 2443
- Decided by: The slope t is 2 or more and the timing gain is above 0.
- Reading: The graded situation is read as the sign of the equal-weight mean of the two raw components, each recomputed per window as value / mean |previous 60 values| x 10 capped at +/-20 (min 20 values), positive meaning the long side; active bars where it cannot be computed are left out; the regression is OLS with intercept on all non-overlapping samples whose 7-bar return stays in the window, the coin's mean being the mean of those samples over all its windows, and the book's before-cost daily gain is the previous bar's post-rebalance allocation x the coin's daily return, averaged over coins each day.
- Size: unusual move +0.85 % per case over 7 bars, 0.063 of the coin's usual move (12.44 %); normal drift in its direction +0.06 %, total +0.91 %; 2241 cases
Plan: `steps_cards/03_test_plan/volume_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d`
Measure: `measure.py`
