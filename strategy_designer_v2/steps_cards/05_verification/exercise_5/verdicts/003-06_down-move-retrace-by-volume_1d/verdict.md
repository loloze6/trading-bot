---
plan: 003-06_down-move-retrace-by-volume_1d
idea: 003-06_down-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: thin-minus-heavy mean next-bar give-back share (next return / |drop|): -2.90899; Welch t: -0.480613 (threshold: difference > 0 with Welch t >= 2 and thin mean > 0 to confirm; difference <= 0 with t <= -1 to reject)
- Supporting check: terciles of drop size where thin-minus-heavy has the overall sign (need >= 2 of 3): 1, passed: False
- Counts: thin down bars: 230, heavy down bars: 146
- Decided by: Inconclusive: a negative difference with Welch t above -1.
- Reading: Thin and heavy down bars are taken from the strategy's own regime label (mean_reversion = thin, trending = heavy) on bars whose in-window close-to-close move is negative, the window's first row (no prior close) and last row (no next close) are dropped, terciles are equal-count cuts of |drop| pooled over both groups, and the reject rule's 'at or below 0' is read together with the inconclusive rule so a negative difference needs t <= -1 (an exactly zero difference rejects).
Plan: `steps_cards/03_test_plan/plans/003-06_down-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-06_down-move-retrace-by-volume_1d`
Measure: `measure.py`
