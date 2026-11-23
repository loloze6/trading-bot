---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of trending-grid 7-bar forward return minus coin mean on forecast: 0.00581864; OLS slope t: 2.21064 (threshold: t >= 2 confirms (with positive timing), t <= -2 rejects)
- Supporting check: book mean daily return minus market-rise gain (timing part) > 0: 0.0007079, passed: True
- Counts: trending grid cases: 177
- Decided by: The slope's t is 2 or more and the timing part is positive.
- Reading: Situation = 30-bar return > 0, read from the recorded mom30 raw value (recomputed from closes inside the window where it is missing). The expected side of this graded long idea is a forecast whose sign follows the equal-weight mean of the three standardised terms, so higher readings give a higher forecast. Each coin's mean 7-bar return is taken over its non-overlapping grid bars in all windows and all regimes. The slope t is the ordinary OLS t. The plan's 'fewer than 100 trending grid cases' is treated as a minimum count, so it gives 'not observable'.
- Size: unusual move +3.97 % per case over 7 bars, 0.208 of the coin's usual move (22.70 %); normal drift in its direction +2.00 %, total +5.97 %; 178 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d.md`
Record: `steps_cards/04_backtest/night_013_run/unseen_2016_2017/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d`
Measure: `measure.py`
