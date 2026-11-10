---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 5-bar return after top-quintile |forecast| minus after neutral bars: -0.00471703; Welch t: -0.47198 (threshold: confirm if difference < 0 with Welch t <= -2; reject if difference > 0 with t >= +2)
- Supporting check: coins with the same sign of the difference (need >= 2): 1, passed: False
- Counts: non-overlapping extreme cases: 77, non-overlapping neutral cases: 160, coins: 2
- Decided by: The t-statistic lies between -2 and +2, so the result is inconclusive.
- Reading: Quintiles of |forecast| are taken over the pooled non-zero-forecast bars on the 5-bar grid (top = at or above the 80th percentile, neutral = forecast 0 or at or below the 20th percentile), and the supporting check requires at least 2 coins with the pooled sign among the coins present (both of the 2 here). It is reported but does not gate the plan's confirm/reject rule.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
