---
plan: 038-01_calm-swing-scaled-rise-continues_1d
idea: 038-01_calm-swing-scaled-rise-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on forecast: 0.000669978; slope t, clustered by date: 1.11755 (threshold: slope t >= 2 with positive mean excess return confirms; slope t <= -2 rejects; else inconclusive; at least 100 grid cases)
- Supporting check: mean 5-bar excess return > 0: -0.00155285, passed: False
- Counts: grid cases with forecast > 0: 1779, dates: 387
- Decided by: The slope's t is between -2 and 2 (inconclusive rule).
- Reading: Grid at positions 0,5,10,... of each window with a full 5-bar forward return; excess = return minus the coin's mean 5-bar return over all grid bars of all its windows; slope t uses OLS with standard errors clustered by date (CR1 correction) to pool same-date cases; the plan's 'fewer than 100 grid cases' minimum is reported as not observable.
- Size: unusual move +0.17 % (t 0.47, the cases of one day together: 897 days) per case over 5 bars, 0.012 of the coin's usual move (11.68 %); normal drift in its direction +0.70 %, total +0.87 %; 2304 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/038-01_calm-swing-scaled-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/038-01_calm-swing-scaled-rise-continues_1d`
Measure: `measure.py`
