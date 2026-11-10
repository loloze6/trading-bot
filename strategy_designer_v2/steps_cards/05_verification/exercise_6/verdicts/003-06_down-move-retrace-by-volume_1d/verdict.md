---
plan: 003-06_down-move-retrace-by-volume_1d
idea: 003-06_down-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: thin minus heavy mean next-bar give-back share (next return / |drop|): -2.90899; Welch t: -0.480613 (threshold: difference > 0 with Welch t >= 2 and thin mean > 0 confirms; difference <= 0 with t <= -1 rejects)
- Supporting check: drop-size terciles (of 3) where thin-minus-heavy has the overall sign; pass if >= 2: 1, passed: False
- Counts: thin down bars: 230, heavy down bars: 146
- Decided by: A negative difference with Welch t above -1.
- Reading: Thin/heavy down bars are taken from the strategy's regime label (mean_reversion = thin, trending = heavy) on bars whose close-to-close move inside the window is negative, terciles are of |drop| pooled over both groups with signs compared to the overall difference, and the overlapping reject/inconclusive rules are reconciled by rejecting a negative difference only when t <= -1 (a zero difference rejects), with a positive t >= 2 difference but non-positive thin mean left inconclusive.
Plan: `steps_cards/03_test_plan/plans/003-06_down-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-06_down-move-retrace-by-volume_1d`
Measure: `measure.py`
