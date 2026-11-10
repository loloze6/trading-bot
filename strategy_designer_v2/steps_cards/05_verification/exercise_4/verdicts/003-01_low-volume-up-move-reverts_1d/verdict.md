---
plan: 003-01_low-volume-up-move-reverts_1d
idea: 003-01_low-volume-up-move-reverts
fit: adapted
status: rejected
---
Evidence:
- Main measure: drift-adjusted position-weighted next-bar return after thin-volume up bars: -0.00081296; t of the mean: -0.517597 (threshold: above 0 with t-stat >= 2.0 to confirm; <= 0 with t-stat <= 0 to reject)
- Supporting check: largest-third minus smallest-third mean drift-adjusted next-bar drop, by |position|: 0.00228312, passed: True
- Counts: qualifying bars: 195, largest third: 65, smallest third: 65
- Decided by: The short earns 0 or less after the drift adjustment with a t-stat of 0 or below.
- Reading: Qualifying bars are rows with regime 'mean_reversion' that have a next close in the same window. The position is postRebalance_current_allocation, the position actually held. Each case is position x (next-bar return minus that window's unconditional mean next-bar return), pooled over all windows. Thirds are a stable sort on |position| split with array_split.
Plan: `steps_cards/03_test_plan/plans/003-01_low-volume-up-move-reverts_1d.md`
Record: `steps_cards/04_backtest/backtests/003-01_low-volume-up-move-reverts_1d`
Measure: `measure.py`
