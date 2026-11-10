---
plan: 003-06_down-move-retrace-by-volume_1d
idea: 003-06_down-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: thin minus heavy mean next-bar give-back share of drop: -2.90899; Welch t: -0.480613 (threshold: difference > 0 with Welch t >= 2 and thin mean share > 0 to confirm; difference <= 0 with t <= -1 to reject)
- Supporting check: terciles of drop size with same-sign thin-minus-heavy difference (of 3): 1, passed: False
- Counts: thin down bars: 230, heavy down bars: 146, thin mean give-back share: -0.705093, heavy mean give-back share: 2.20389
- Decided by: A positive difference with t below 2 (or thin mean not above 0), or a negative difference with t above -1, so the test is inconclusive.
- Reading: Thin/heavy down bars are taken from the strategy's regime label (mean_reversion = thin, trending = heavy) with the drop computed as close[t]/close[t-1]-1 < 0 inside each window (a window's first row has no drop and is left out); because the reject and inconclusive rules overlap for negative differences, a negative difference rejects only when Welch t <= -1 (or the difference is exactly 0), and the supporting check counts terciles (equal-count by pooled |drop|) whose difference has the main difference's sign and is reported without changing the verdict.
Plan: `steps_cards/03_test_plan/plans/003-06_down-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-06_down-move-retrace-by-volume_1d`
Measure: `measure.py`
