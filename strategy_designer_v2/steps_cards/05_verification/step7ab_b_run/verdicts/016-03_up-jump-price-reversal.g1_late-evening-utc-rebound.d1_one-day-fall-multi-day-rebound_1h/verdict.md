---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 72-bar excess return (vs coin mean 72-bar return) on forecast, grid 0,72,144,...: 0.000313068; OLS slope t: 1.92024 (threshold: confirm: slope > 0 with t >= 2 and timing check > 0; reject: slope < 0 with t <= -2)
- Supporting check: book mean daily return minus market-rise gain (timing): -4.24127e-05, passed: False
- Counts: grid cases with forecast > 0: 2810, grid cases in total: 5683
- Decided by: The slope's t-statistic lies between -2 and 2.
- Reading: The slope comes from OLS with an intercept, pooled over all grid bars that have a full 72-bar forward return in their window; the coin's mean 72-bar return is the mean of its grid returns over all windows; the position behind each day's market gain is the mean of the positions held over that day's bars; and the plan's 'fewer than 200 cases' rule is reported as not observable, as the instructions require.
- Size: unusual move +0.06 % per case over 72 bars, 0.008 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.47 %; 5588 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h.md`
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h`
Measure: `measure.py`
