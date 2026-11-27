---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 96-bar move of long bets (return minus coin's mean 96-bar return): 0.00863518; t of the mean: 4.07663 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject; at least 30 independent cases)
- Supporting check: Spearman rank correlation of forecast at case bar vs unusual move > 0: 0.0274425, passed: True
- Counts: independent cases: 4671
- Decided by: Mean unusual move positive with t >= 2 over at least 30 independent cases, and the Spearman correlation is above 0.
- Reading: Situation = raw component > 0 (24h fall with positive 30-day return, recomputed from prices where the raw value is missing) on the long side; cases are long bets (forecast rise >= 2 from its lowest positive level since the last bet, from 0 after a flat), the first one in each 96-bar grid cell of a window counted from its first row, kept only if the 96-bar forward return stays inside the window; the drift is the coin's mean return on the 0, 96, 192, ... grid of all its windows.
- Size: unusual move +0.86 % (t 2.84, the cases of one day together: 1726 days) per case over 96 bars, 0.072 of the coin's usual move (10.82 %); normal drift in its direction +0.87 %, total +1.73 %; 4671 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend_1h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend_1h`
Measure: `measure.py`
