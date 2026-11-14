---
plan: N2-04_slow-and-fast-momentum_1d_oos
idea: N2-04_slow-and-fast-momentum
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean 20-bar forward excess return (vs coin mean) on active bars, non-overlapping, pooled: 0.00455682; t of the mean: 0.224986 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; inconclusive otherwise or if fewer than 30 blocks)
- Supporting check: OLS slope of 20-bar excess return on forecast level (active, non-overlapping): 0.00667264, passed: True
- Counts: non-overlapping 20-bar active blocks: 177
- Decided by: The t-statistic lies between -2 and 2, meeting neither the confirm nor the reject rule.
- Reading: The coin's mean 20-bar return uses every bar's in-window 20-bar forward return across all its windows (overlapping), active blocks are grid bars 0, 20, 40, ... of each window with forecast > 0 and a full 20-bar forward return, and the supporting slope is reported but not used in the decision rule.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N2-04_slow-and-fast-momentum_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N2-04_slow-and-fast-momentum_1d_oos`
Measure: `measure.py`
