---
plan: N2-04_slow-and-fast-momentum_1d_oos2
idea: N2-04_slow-and-fast-momentum
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 20-bar forward excess return over coin mean, active bars, non-overlapping: 0.0651757; t of the mean: 0.540099 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; else inconclusive; at least 30 non-overlapping active blocks)
- Supporting check: slope of 20-bar excess return on forecast level (non-overlapping active blocks): 0.00412571, passed: True
- Counts: non-overlapping 20-bar active blocks: 69
- Decided by: The t-statistic lies between -2 and 2, meeting the plan's inconclusive rule.
- Reading: The coin's mean 20-bar return is taken over every bar of all its windows (overlapping, within windows); the active blocks are the active bars (forecast > 0) on the grid 0, 20, 40, ... of each window; the situation is checked on the raw slow/medium returns, using the regime label where they are missing.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N2-04_slow-and-fast-momentum_1d_oos2.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N2-04_slow-and-fast-momentum_1d_oos2`
Measure: `measure.py`
