---
plan: 018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound_1h
idea: 018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 72-bar unusual move of the long cases (return minus coin's normal 72-bar drift): -0.00148685; t of the mean: -0.741392 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: deeper-half minus shallower-half mean unusual move (Welch difference > 0): 0.000841869, passed: True
- Counts: cases: 2167, deeper half cases: 782, shallower half cases: 782
- Decided by: Main t between -2 and 2 over at least 30 cases.
- Reading: Bets are long forecast rises of >= 2 points from the lowest level since the last bet, the first per 72-bar grid cell of each window counted from its first row; depth uses the 720 closes including the current bar within the window, cases or bars without 720 closes of history are left out of the depth measures; the deeper half is depth strictly below the median and the shallower half the rest; the check passes on the sign of the difference (Welch t reported as supporting information only).
- Size: unusual move -0.15 % per case over 72 bars, -0.015 of the coin's usual move (8.23 %); normal drift in its direction +0.43 %, total +0.28 %; 2167 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound_1h`
Measure: `measure.py`
