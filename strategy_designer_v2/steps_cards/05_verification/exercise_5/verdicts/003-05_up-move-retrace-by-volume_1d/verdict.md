---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean next-bar share of move, thin minus heavy: -59.408; Welch t (thin minus heavy): -0.993674 (threshold: thin mean below heavy mean with Welch t of at least 2.0 (t <= -2.0 for thin minus heavy), and thin mean below 0)
- Supporting check: min of mean active-bar strategy return before costs over heavy-only and thin-only parts (vs holding BTC): -0.000608976, passed: False
- Counts: thin cases: 145, heavy cases: 120
- Decided by: Inconclusive: thin is below heavy but the Welch t-stat is under 2.0 in magnitude.
- Reading: Sharp-move bars are those labelled mean_reversion (thin) or trending (heavy), with the move as close[t]/close[t-1]-1 inside the window and only positive moves with a next bar in the same window kept. The supporting check passes when the mean active-bar strategy return (allocation != 0) is positive in both the heavy and thin parts, with the BTC hold return reported alongside. Thin significantly below heavy but not below 0 matches no rule literally and is reported as inconclusive.
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
