---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 96-bar move of long bets (return minus coin's mean 96-bar return): 0.012516; t of the mean: 1.45788 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject; at least 30 independent cases)
- Supporting check: Spearman rank correlation of forecast at case bar vs unusual move > 0: -0.052156, passed: False
- Counts: independent cases: 392
- Decided by: t lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: Situation = raw component > 0 (24h fall with positive 30-day return, recomputed from prices where the raw value is missing) on the long side; cases are long bets (forecast rise >= 2 from its lowest positive level since the last bet, from 0 after a flat), the first one in each 96-bar grid cell of a window counted from its first row, kept only if the 96-bar forward return stays inside the window; the drift is the coin's mean return on the 0, 96, 192, ... grid of all its windows.
- Size: unusual move +1.25 % per case over 96 bars, 0.083 of the coin's usual move (18.05 %); normal drift in its direction +4.05 %, total +5.31 %; 392 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/unseen_2016_2017/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend_1h`
Measure: `measure.py`
