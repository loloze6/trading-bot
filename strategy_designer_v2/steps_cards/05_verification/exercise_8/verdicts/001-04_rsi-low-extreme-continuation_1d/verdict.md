---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean fwd 5-bar return after top-quintile |forecast| minus after neutral bars: -0.00147462; Welch t: -0.139197 (threshold: confirm if difference < 0 with Welch t <= -2; reject if > 0 with t >= +2; else inconclusive; min 30 extreme cases)
- Supporting check: number of coins whose difference has the pooled sign (need >= 2): 1, passed: False
- Counts: non-overlapping extreme cases: 77, non-overlapping neutral cases: 129, coins: 2
- Decided by: Welch t lies between -2 and +2, so inconclusive.
- Reading: Quintiles of |forecast| are taken over all pooled non-overlapping grid bars (extreme = |forecast| at or above the 80th percentile and non-zero, neutral = forecast 0 or at or below the 20th percentile), and the supporting check needs 2 coins with the pooled sign whatever the number of coins present.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
