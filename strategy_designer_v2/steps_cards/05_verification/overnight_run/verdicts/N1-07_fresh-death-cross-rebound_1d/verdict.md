---
plan: N1-07_fresh-death-cross-rebound_1d
idea: N1-07_fresh-death-cross-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar forward return on fresh-death-cross bars minus coin's mean 10-bar return: 0.0107199; t clustered by cross event: 0.906337 (threshold: confirm if above 0 with t >= +2 and supporting check positive; reject if below 0 with t <= -2)
- Supporting check: allocation-weighted 1-bar return on regime bars minus coin's mean 1-bar return: 0.00133268, passed: True
- Counts: distinct death-cross events: 62, non-overlapping 10-bar blocks: 110
- Decided by: Enough events and blocks, but the numbers meet neither the confirm rule nor the reject rule (t between -2 and +2, or confirm's supporting check not positive).
- Reading: Regime bars are those labelled mean_reversion, blocks are the window grid bars 0,10,20,... on those bars, holding is the coin's mean grid 10-bar return over all its windows, an event is one contiguous run of regime bars in a window and the clustered t uses the CR1 cluster variance of the mean, both minimums (15 events and 30 blocks) must be reached, and the supporting check is sum(alloc x (1-bar return - coin's mean 1-bar return)) / sum(alloc) over regime bars.
Plan: `steps_cards/03_test_plan/overnight_run/plans_newcomp/N1-07_fresh-death-cross-rebound_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-07_fresh-death-cross-rebound_1d`
Measure: `measure.py`
