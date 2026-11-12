---
plan: 001-04_rsi-low-extreme-continuation_1d
idea: 001-04_rsi-low-extreme-continuation
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 5-bar return after top-quintile |forecast| minus after neutral bars: -0.00471703; Welch t: -0.47198 (threshold: confirm if difference < 0 with Welch t <= -2; reject if difference > 0 with t >= +2)
- Supporting check: coins whose difference has the pooled sign (need >= 2): 1, passed: False
- Counts: non-overlapping extreme cases: 77, non-overlapping neutral cases: 160, coins: 2
- Decided by: The Welch t of the difference lies between -2 and +2.
- Reading: Quintiles of |forecast| are taken over the nonzero-forecast grid bars pooled across coins and windows (extreme = at or above the 80th percentile, neutral = forecast 0 or at or below the 20th percentile), the supporting check counts the coins present (2 of the record's coins) whose difference has the pooled sign and is reported without entering the decision since the confirm rule does not name it, and a missing Welch t for lack of neutral cases is treated as not observable.
Plan: `steps_cards/03_test_plan/plans/001-04_rsi-low-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-04_rsi-low-extreme-continuation_1d`
Measure: `measure.py`
