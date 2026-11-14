---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean next-bar return / move return, thin minus heavy: -59.408; Welch t (thin minus heavy): -0.993674 (threshold: thin mean share below heavy with Welch t of at least 2.0 in magnitude, and thin mean share below 0)
- Supporting check: min over heavy-only and thin-only parts of mean active-bar gain before costs minus BTC return: -0.000952798, passed: False
- Counts: thin cases: 145, heavy cases: 120, thin mean share: -59.5677, heavy mean share: -0.159689, heavy-only active bars: 138, thin-only active bars: 169, heavy-only mean excess: -0.000952798, thin-only mean excess: 0.000882208
- Decided by: Thin mean share is below heavy but the Welch t-stat is under 2.0, so the result is inconclusive.
- Reading: Bars are classified by the recorded regime label (mean_reversion = thin, trending = heavy). The move is close[t]/close[t-1]-1 within the window, so each window's first row and any non-positive moves are dropped. The Welch t is taken as thin minus heavy and needs to be at or below -2.0. If thin is significantly below heavy but thin is at or above 0, the plan's second reject clause applies. The supporting check compares the per-bar allocation gain minus the BTC return on bars with a non-zero position in each regime.
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
