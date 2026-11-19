---
plan: 016-05_up-even-volume-continuation_1h
idea: 016-05_up-even-volume-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: top-third minus bottom-third mean excess 72-bar forward return (by forecast): 0.00265188; Welch t: 0.676444 (threshold: Welch t >= 2 confirms (with top-third excess > 0); Welch t <= -2 rejects)
- Supporting check: top-third mean excess 72-bar return > 0: 0.00410629, passed: True
- Counts: grid cases (trending, forecast > 0): 2916, top third grid cases: 972, bottom third grid cases: 972
- Decided by: Welch t of the top-minus-bottom difference lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation check uses only bars whose 72-bar-back close lies inside the same window (the first 72 bars of each window are left out of it). Thirds are the floor(n/3) lowest and highest forecasts of the pooled grid cases (stable sort by forecast). Each coin's mean 72-bar return is the mean over its non-overlapping 72-bar grid of all windows. Trending bars are those with regime 'trending'. Fewer than 30 cases in a third is reported as not observable.
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-05_up-even-volume-continuation_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-05_up-even-volume-continuation_1h`
Measure: `measure.py`
