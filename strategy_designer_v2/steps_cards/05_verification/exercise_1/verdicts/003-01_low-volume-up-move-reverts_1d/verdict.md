---
plan: 003-01_low-volume-up-move-reverts_1d
idea: 003-01_low-volume-up-move-reverts
fit: adapted
status: rejected
---
Evidence:
- Main measure: drift-adjusted, position-weighted next-bar return of the short (mean per case): -0.00081296 (threshold: above 0 with t-stat >= 2.0 to confirm; <= 0 with t-stat <= 0 to reject)
- Supporting check: largest-third minus smallest-third (by |position|) mean drift-adjusted next-bar drop: 0.00228312, passed: True
- Cases: 195
- Decided by: Reject rule: the short earns 0 or less after the drift adjustment, with a t-stat of 0 or below.
- Reading: A case is a bar labelled regime 'mean_reversion' with a next bar in the same window. Its value is postRebalance_current_allocation x (next-bar return minus that window's unconditional mean next-bar return), and cases with a zero position count with value 0. The t-stat is the mean over its standard error, pooled over all windows. Thirds come from a stable sort by |position|.
Plan: `steps_cards/03_test_plan/plans/003-01_low-volume-up-move-reverts_1d.md`
Record: `steps_cards/04_backtest/backtests/003-01_low-volume-up-move-reverts_1d`
Measure: `measure.py`
