---
plan: 003-01_low-volume-up-move-reverts_1d
idea: 003-01_low-volume-up-move-reverts
fit: adapted
status: rejected
---
Evidence:
- Main measure: drift-adjusted position-weighted next-bar return of the short (t-stat): -0.517597 (threshold: mean above 0 with t-stat >= 2.0 to confirm; mean <= 0 with t-stat <= 0 to reject; at least 60 cases)
- Supporting check: largest-third minus smallest-third next-bar drop vs unconditional mean (by |position|): 0.00228312, passed: True
- Cases: 195
- Decided by: The short earns 0 or less after the drift adjustment with a t-stat of 0 or below.
- Reading: Thin up bars are rows labelled regime 'mean_reversion'; each case's value is postRebalance_current_allocation x (next-bar return minus the window's mean next-bar return), pooled across all windows, with the main value reported as the t-stat of these values (mean -0.0008129600837140532); thirds are split by sorted |position| with numpy array_split.
Plan: `steps_cards/03_test_plan/plans/003-01_low-volume-up-move-reverts_1d.md`
Record: `steps_cards/04_backtest/backtests/003-01_low-volume-up-move-reverts_1d`
Measure: `measure.py`
