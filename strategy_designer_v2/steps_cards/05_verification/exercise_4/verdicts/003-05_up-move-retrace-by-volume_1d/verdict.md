---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean next-bar share of the move, thin minus heavy: -44.5479; Welch t (thin minus heavy): -1.07692 (threshold: thin mean share below heavy mean share with Welch t of at least 2.0 in magnitude (thin below heavy), and thin mean share below 0)
- Supporting check: strategy minus BTC hold return on active bars, min of heavy-only and thin-only parts: -0.00315756, passed: False
- Counts: thin cases: 211, heavy cases: 146, thin mean share: -44.7469, heavy mean share: -0.199033
- Decided by: Inconclusive: thin is below heavy but the Welch t-stat is under 2.0.
- Reading: Thin cases are bars labelled mean_reversion and heavy cases bars labelled trending, with the move as close[t]/close[t-1]-1 and the next return close[t+1]/close[t]-1 inside the window. The supporting check is read as the summed before-cost position gain minus BTC's summed return on each part's bars, which must be above 0 in both parts. A t-stat of at least 2.0 with the thin mean not below 0 meets neither the confirm nor the reject rule, so it is treated as inconclusive.
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
