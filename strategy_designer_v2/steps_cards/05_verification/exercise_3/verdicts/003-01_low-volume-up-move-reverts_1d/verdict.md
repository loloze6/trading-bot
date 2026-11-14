---
plan: 003-01_low-volume-up-move-reverts_1d
idea: 003-01_low-volume-up-move-reverts
fit: adapted
status: rejected
---
Evidence:
- Main measure: drift-adjusted position-weighted next-bar return of the short after thin up bars: -0.00081296; t of the mean: -0.517597 (threshold: above 0 with t-stat >= 2.0 to confirm; <= 0 with t-stat <= 0 to reject)
- Supporting check: largest minus smallest |position| third, mean drift-adjusted next-bar drop: 0.00228312, passed: True
- Counts: qualifying bars: 195, windows: 6
- Decided by: The short earns 0 or less after the drift adjustment with a t-stat of 0 or below.
- Reading: Cases are all bars with regime 'mean_reversion' (thin up bars) having a next bar in the same window, each case's value is postRebalance_current_allocation x (next-bar return minus the window's unconditional mean next-bar return) averaged over pooled cases with the ordinary t of the mean, and thirds are formed by a stable sort on |postRebalance_current_allocation| split into three near-equal groups.
Plan: `steps_cards/03_test_plan/plans/003-01_low-volume-up-move-reverts_1d.md`
Record: `steps_cards/04_backtest/backtests/003-01_low-volume-up-move-reverts_1d`
Measure: `measure.py`
