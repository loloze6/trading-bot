---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean next-bar share of move, thin minus heavy: -59.408; Welch t (thin minus heavy): -0.993674 (threshold: thin mean share below heavy mean share with Welch t of at least 2.0 in magnitude, and thin mean share below 0)
- Supporting check: strategy minus holding BTC on active bars, min of heavy-only and thin-only parts: -0.131486, passed: False
- Counts: thin cases: 145, heavy cases: 120
- Decided by: Thin is below heavy but the Welch t-stat magnitude is under 2.0, so the result is inconclusive.
- Reading: Heavy and thin cases are the bars labelled trending and mean_reversion. The move is the bar's own close-to-close return inside its window, and only moves above 0 are kept. The t-stat compares thin minus heavy, so a value of -2.0 or lower counts as at least 2.0. The case where thin is significantly below heavy but not below 0 matches no rule and is treated as inconclusive. The supporting check sums the strategy's gain minus BTC's return over active bars (allocation not 0), split by regime, and is reported but does not enter the decision.
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
