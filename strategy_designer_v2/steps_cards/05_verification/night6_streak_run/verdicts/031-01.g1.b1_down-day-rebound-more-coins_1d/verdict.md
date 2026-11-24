---
plan: 031-01.g1.b1_down-day-rebound-more-coins_1d
idea: 031-01.g1.b1_down-day-rebound-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 3-day return minus drift on forecast (grid bars, forecast > 0, pooled): 0.000179235; slope t clustered by day: 0.400115 (threshold: confirm: slope > 0 with t >= 2 (and mean unusual move > 0); reject: slope < 0 with t <= -2)
- Supporting check: mean unusual move of the bets, before costs: 0.00021989, passed: True
- Counts: grid cases: 5730, distinct days: 814, bet cases: 9265
- Decided by: The slope's t lies between -2 and 2.
- Reading: The situation is a raw scaled return below 0 with a positive forecast; the drift is each coin's mean non-overlapping 3-bar return over all its windows; the slope is OLS with intercept and its t uses day-clustered errors with a G/(G-1) factor; the supporting check uses the first bet (forecast rise >= 2 points) per 3-bar grid cell; the plan's 'fewer cases' rule is reported as not observable.
- Size: unusual move +0.02 % (t 0.10, the cases of one day together: 1763 days) per case over 3 bars, 0.004 of the coin's usual move (9.14 %); normal drift in its direction +0.46 %, total +0.48 %; 9265 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-01.g1.b1_down-day-rebound-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.g1.b1_down-day-rebound-more-coins_1d`
Measure: `measure.py`
