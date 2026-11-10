---
plan: 002-05_short-above-long-sma-drift-up_1h
idea: 002-05_short-above-long-sma-drift-up
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess 24-bar forward return in zone over all-bar mean: -0.000194076; Welch t: -0.109065 (threshold: positive with t >= 2 and >= 4 of 6 windows positive to confirm; negative with t <= -2 to reject)
- Supporting check: in-zone minus all-block share of positive 24-bar blocks: -0.0216073, passed: False
- Counts: non-overlapping in-zone 24-bar blocks pooled: 348, all non-overlapping 24-bar blocks pooled: 724, windows with positive excess: 4, windows: 6
- Decided by: The t lies strictly between -2 and +2, so the result is inconclusive.
- Reading: Blocks start at positions 0, 24, 48... of each window and are in-zone when forecast > 0 at the block start; each block return is demeaned by its window's all-block mean, the pooled excess is the mean of in-zone demeaned returns tested by Welch t against all demeaned blocks; a window with no in-zone blocks counts as not positive; the supporting check passes at a difference >= 0 and does not enter the decision.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-05_short-above-long-sma-drift-up_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-05_short-above-long-sma-drift-up_1h`
Measure: `measure.py`
