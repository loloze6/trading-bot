---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: thin minus heavy mean next-bar share of move (heavy mean - thin mean), Welch t: 44.5479 (threshold: thin mean share below heavy mean share with Welch t >= 2.0, and thin mean share below 0)
- Supporting check: active-bar gain before costs minus holding BTC, heavy-only and thin-only parts (min of the two): -0.131486, passed: False
- Cases: 357
- Decided by: Inconclusive: thin mean share is below heavy but the Welch t-stat is under 2.0.
- Reading: Sharp-move bars are those labelled regime 'trending' (heavy) or 'mean_reversion' (thin); the move is close[t]/close[t-1]-1 within the window (so a window's first bar and last bar drop out); the supporting check sums per-bar position gain minus BTC return over active bars (non-zero held allocation) split by the bar's regime label, and does not change the status; thin below heavy with t >= 2 but thin share >= 0 meets no stated rule and is reported inconclusive.
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
