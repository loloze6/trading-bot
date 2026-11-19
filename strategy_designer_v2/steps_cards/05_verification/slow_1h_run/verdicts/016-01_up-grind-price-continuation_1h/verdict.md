---
plan: 016-01_up-grind-price-continuation_1h
idea: 016-01_up-grind-price-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: next-72-bar return, top third minus bottom third of forecast (>0) on the 72-bar grid: -0.00427184; Welch t: -0.569328 (threshold: Welch t >= 2 confirms (with supporting check), Welch t <= -2 rejects)
- Supporting check: top third mean next-72-bar return minus holding-the-coin mean 72-bar return: 0.0084474, passed: True
- Counts: grid cases in top third: 316, grid cases in bottom third: 316, grid cases with forecast above 0: 947
- Decided by: The top-minus-bottom Welch t lies between -2 and 2.
- Reading: Thirds are equal-size splits of the pooled grid cases sorted by forecast (ties kept in coin/window/time order), and the holding benchmark for the pooled top third is the mean, over its cases, of each case's coin mean 72-bar grid return over all windows; the situation is a positive raw residual share on the long side.
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-01_up-grind-price-continuation_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-01_up-grind-price-continuation_1h`
Measure: `measure.py`
