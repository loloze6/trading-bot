---
plan: 003-06_down-move-retrace-by-volume_1d
idea: 003-06_down-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean next-bar give-back share (next return / |drop|), thin minus heavy down bars: -2.90899 (threshold: thin-minus-heavy > 0 with Welch t >= 2 and thin mean > 0 (reject: <= 0 with t <= -1))
- Supporting check: same-sign thin-minus-heavy difference in terciles of drop size (of 3, need >= 2): 1, passed: False
- Cases: 376
- Decided by: Inconclusive: a negative difference with a t-statistic above -1.
- Reading: Thin and heavy down bars are taken from the strategy's regime label (mean_reversion = thin, trending = heavy) on bars whose own close-to-close move inside the window is negative and whose next close is in the same window; terciles are cut on |drop| pooled across both groups; since the reject and inconclusive rules overlap, a negative difference with t above -1 is inconclusive and the reject rule needs t of -1 or lower (or a difference of exactly 0); a positive difference with t >= 2 but a thin mean <= 0 is inconclusive; the supporting check is reported but does not change the status, as the plan's rules do not use it.
Plan: `steps_cards/03_test_plan/plans/003-06_down-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-06_down-move-retrace-by-volume_1d`
Measure: `measure.py`
