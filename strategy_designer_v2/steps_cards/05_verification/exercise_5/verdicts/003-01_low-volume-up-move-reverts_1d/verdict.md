---
plan: 003-01_low-volume-up-move-reverts_1d
idea: 003-01_low-volume-up-move-reverts
fit: adapted
status: rejected
---
Evidence:
- Main measure: drift-adjusted position-weighted next-bar return of the short after thin up bars: -0.00139336; t of the mean of drift-adjusted position gains: -0.517597 (threshold: above 0 with t-stat >= 2.0 to confirm; <= 0 with t-stat <= 0 to reject)
- Supporting check: mean next-bar drop vs unconditional mean, largest third minus smallest third by |position|: 0.00228312, passed: True
- Counts: qualifying bars: 195
- Decided by: The short earns 0 or less after the drift adjustment, with a t-stat of 0 or below.
- Reading: Cases are bars labelled regime 'mean_reversion' with a next bar in the same window, the position is postRebalance_current_allocation (zero positions kept as cases), the main value is sum(pos x (r - window mean)) / sum(|pos|) so a short gains when r falls below the mean, its t-stat is the ordinary t of the per-case gains pos x (r - mean), and thirds are the n//3 cases with smallest and largest |position|.
Plan: `steps_cards/03_test_plan/plans/003-01_low-volume-up-move-reverts_1d.md`
Record: `steps_cards/04_backtest/backtests/003-01_low-volume-up-move-reverts_1d`
Measure: `measure.py`
