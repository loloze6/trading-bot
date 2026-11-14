---
plan: N2-04_slow-and-fast-momentum_1d
idea: N2-04_slow-and-fast-momentum
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean 20-bar forward excess return over the coin's mean 20-bar return, active bars, non-overlapping: 0.0190129; t of the mean: 0.849656 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 non-overlapping active blocks)
- Supporting check: OLS slope of 20-bar excess return on forecast level, active non-overlapping blocks: 0.00404784, passed: True
- Counts: non-overlapping 20-bar active blocks pooled across coins and windows: 269
- Decided by: The t-statistic lies between -2 and 2.
- Reading: Situation checked on the regime label 'trending' plus both 60- and 20-bar close returns > 0 where computable inside the window, long side = forecast > 0; the coin's mean 20-bar return and the active samples use the same non-overlapping grid (positions 0, 20, 40, ... of each window), an active block is a grid bar with forecast > 0 and a full 20-bar forward return, and the supporting slope is an OLS of excess return on forecast over those same blocks.
Plan: `steps_cards/03_test_plan/plans/N2-04_slow-and-fast-momentum_1d.md`
Record: `steps_cards/04_backtest/backtests/N2-04_slow-and-fast-momentum_1d`
Measure: `measure.py`
