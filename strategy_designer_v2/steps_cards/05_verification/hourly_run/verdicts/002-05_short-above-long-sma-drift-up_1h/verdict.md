---
plan: 002-05_short-above-long-sma-drift-up_1h
idea: 002-05_short-above-long-sma-drift-up
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled excess 24-bar forward return in zone (forecast > 0) over the window's all-block mean: -0.000194076; t of the mean of pooled per-block excess: -0.13627 (threshold: confirm: excess > 0 with t >= 2 and >= 4 of 6 windows positive; reject: excess < 0 with t <= -2; at least 150 in-zone blocks)
- Supporting check: share of positive in-zone blocks minus share over all blocks (>= 0): -0.0216073, passed: False
- Counts: non-overlapping in-zone 24-bar blocks pooled: 348, windows with positive excess: 4, windows with in-zone blocks: 6
- Decided by: Inconclusive: t lies strictly between -2 and +2 (or sign and t disagree).
- Reading: Blocks start at positions 0, 24, 48, ... of each window and are in-zone when forecast > 0 at the block start; each in-zone return is reduced by the mean of all blocks of its window, and the pooled excesses are tested with the ordinary t of the mean; a window counts as positive if its mean excess is > 0; the supporting check passes at a difference >= 0 and does not decide the status.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-05_short-above-long-sma-drift-up_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-05_short-above-long-sma-drift-up_1h`
Measure: `measure.py`
