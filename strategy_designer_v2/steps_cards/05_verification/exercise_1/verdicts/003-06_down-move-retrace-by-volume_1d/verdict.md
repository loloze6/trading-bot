---
plan: 003-06_down-move-retrace-by-volume_1d
idea: 003-06_down-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: thin-minus-heavy mean next-bar give-back share (next return / |drop|): -2.90899 (threshold: above 0 with Welch t >= 2 (and thin mean > 0) to confirm; at or below 0 with t <= -1 to reject)
- Supporting check: terciles of drop size with the same sign of thin-minus-heavy difference (need >= 2 of 3): 1, passed: False
- Cases: 376
- Decided by: A negative difference with a Welch t above -1 is inconclusive.
- Reading: Thin and heavy down bars are taken from the strategy's regime label (mean_reversion = thin, trending = heavy) on bars whose close-to-close move within the window is negative, so the first bar of each window is left out; the reject rule's 'at or below 0' is read together with the inconclusive rule, so a negative difference rejects only with t <= -1 while a zero difference rejects; 'same sign' in terciles means the same sign as the pooled difference, and a tercile missing either group does not count.
Plan: `steps_cards/03_test_plan/plans/003-06_down-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-06_down-move-retrace-by-volume_1d`
Measure: `measure.py`
