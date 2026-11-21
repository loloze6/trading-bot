---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of coin-demeaned non-overlapping 7-bar forward return on forecast: 0.00079133; OLS slope t: 3.26246 (threshold: confirm: slope > 0 with t >= 2 and timing gain > 0; reject: slope < 0 with t <= -2)
- Supporting check: book mean daily gain before costs minus gain from market's own rise (timing): 0.000617278, passed: True
- Counts: non-overlapping cases: 2443
- Decided by: Slope positive with t >= 2 and the timing part of the book's gain is above 0.
- Reading: Each coin's mean 7-bar return is the mean of its non-overlapping grid returns over all windows; the book's gain before costs is the held allocation times the next close-to-close return, averaged over coins per day, and its market part uses each coin's mean daily return over all windows.
- Size: unusual move +0.81 % per case over 7 bars, 0.058 of the coin's usual move (12.44 %); normal drift in its direction -0.00 %, total +0.81 %; 2188 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation_1d`
Measure: `measure.py`
