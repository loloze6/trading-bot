---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 10-bar forward return on short bars minus mean over all bars: 0.466185; Welch t: 0.235475 (threshold: at most -1.0% per 10 bars with t-stat of -2 or lower)
- Supporting check: falling share on short blocks minus unconditional falling share (points): 3.15271, passed: False
- Counts: non-overlapping 10-bar short blocks: 29, non-overlapping 10-bar blocks (all bars): 70, distinct downward crosses: 2
- Decided by: Rejected: the difference is 0 or above, or the falling share on short bars is not above the unconditional share.
- Reading: Blocks are the bars at positions 0, 10, 20, ... of each window with a forward return inside the window, short blocks are those with forecast < 0 at the block start, the difference is in percent and tested with Welch's t against all blocks, and a distinct downward cross is a move of the forecast from >= 0 to < 0 between consecutive bars inside a window; the minimum counts are checked first, then confirm, then reject, else inconclusive.
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
