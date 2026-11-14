---
plan: 003-01_low-volume-up-move-reverts_1d
idea: 003-01_low-volume-up-move-reverts
fit: adapted
status: rejected
---
Evidence:
- Main measure: drift-adjusted |position|-weighted next-bar short return after thin up bars: -0.00139336; t of the mean of |position| x drift-adjusted short return: -0.517597 (threshold: above 0 with t-stat >= 2.0 to confirm; at or below 0 with t-stat <= 0 to reject)
- Supporting check: mean drift-adjusted next-bar drop, largest third minus smallest third by |position|: 0.00228312, passed: True
- Counts: qualifying bars: 195, windows: 6
- Decided by: The short earns 0 or less after the drift adjustment with a t-stat of 0 or below.
- Reading: Qualifying bars are rows labelled regime 'mean_reversion' with a next bar in the same window, weighted by |postRebalance_current_allocation| (zero-position bars included with zero weight); the short's gain is minus (next-bar return minus the window's mean next-bar return over all bars), the t-stat is the ordinary t of the per-case products |position| x that gain, and thirds come from an ascending sort by |position| split with array_split.
Plan: `steps_cards/03_test_plan/plans/003-01_low-volume-up-move-reverts_1d.md`
Record: `steps_cards/04_backtest/backtests/003-01_low-volume-up-move-reverts_1d`
Measure: `measure.py`
