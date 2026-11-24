---
plan: 031-01.g1_volatility-scaled-down-day-rebound_1d
idea: 031-01.g1_volatility-scaled-down-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of drift-removed, usual-move-scaled 3-day return on forecast: 0.00401323; day-clustered t of slope: 1.05094 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, between is inconclusive)
- Supporting check: mean unusual 3-day move of long cases (forecast rises >= 2 points): 0.000970936, passed: True
- Counts: grid bars with a forecast above 0: 2718, grid bars: 5723, cases: 4415, days with cases: 1471, days clustered: 1034
- Decided by: The slope's t is between -2 and 2.
- Reading: The regression has an intercept and uses a CR1 day-clustered standard error on grid bars 0,3,6,... of each window with a full 3-bar return, drift and usual move are the mean and std of those same non-overlapping 3-day returns per coin over all windows, cases are read once per 3-bar grid cell (first case in the cell), and the plan's 'fewer than 100 grid bars with a forecast above 0' is reported as not observable.
- Size: unusual move +0.10 % (t 0.43, the cases of one day together: 1471 days) per case over 3 bars, 0.012 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.46 %; 4415 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-01.g1_volatility-scaled-down-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.g1_volatility-scaled-down-day-rebound_1d`
Measure: `measure.py`
