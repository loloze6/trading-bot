---
plan: 010-01_rsi-above-midpoint-continues-up_1d
idea: 010-01_rsi-above-midpoint-continues-up
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 7-bar forward return minus coin mean on forecast, non-overlapping samples: 0.000628876; OLS slope t: 1.82336 (threshold: t >= 2 confirms (with timing check), t <= -2 rejects, at least 300 independent cases)
- Supporting check: book mean daily timing gain before costs: 0.000924257, passed: True
- Counts: independent cases: 815
- Decided by: The slope's t is between -2 and 2, which neither confirms nor rejects.
- Reading: The coin's mean 7-bar return is the mean of its non-overlapping 7-bar samples over all windows, the regression has an intercept, and the per-coin book before costs earns the held allocation x the coin's daily return, averaged over coins each day, with the market part being the allocation x the coin's mean daily return over all windows.
- Size: unusual move +1.51 % per case over 7 bars, 0.130 of the coin's usual move (11.06 %); normal drift in its direction -0.08 %, total +1.42 %; 342 cases
Plan: `steps_cards/03_test_plan/night_run/plans/010-01_rsi-above-midpoint-continues-up_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/010-01_rsi-above-midpoint-continues-up_1d`
Measure: `measure.py`
