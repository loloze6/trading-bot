---
plan: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h
idea: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of forward 72-bar excess return on er72 forecast (pooled trending grid bars): 0.000320248; OLS slope t: 1.25049 (threshold: slope t >= 2 confirms (with top-minus-bottom third > 0); t <= -2 rejects)
- Supporting check: top-third minus bottom-third mean forward 72-bar excess return: 0.00153813, passed: True
- Counts: independent trending grid cases: 2916, top third cases: 972, bottom third cases: 972
- Decided by: Slope t = 1.25 lies between -2 and 2, inconclusive per the plan.
- Reading: The coin's mean 72-bar return is the mean of the forward 72-bar returns on every grid bar (positions 0, 72, 144, ... of each window, all regimes) over all its windows; the slope's t is the OLS slope over its standard error with the pooled trending grid cases; the top and bottom thirds are the floor(n/3) highest and lowest forecasts by sort order; the plan's 'fewer than 100 independent trending grid cases' is treated as the minimum count (not observable); for the situation check, ret72 is recomputed from closes and, on a window's first 72 bars where it cannot be, the recorded regime is used.
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h`
Measure: `measure.py`
