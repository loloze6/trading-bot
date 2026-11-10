---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 10-bar forward return on short bars minus mean over all bars (non-overlapping blocks): 0.466185; Welch t: 0.235475 (threshold: at most -1.0% per 10 bars with t-stat of -2 or lower to confirm; 0 or above rejects)
- Supporting check: falling share on short blocks minus falling share on all blocks (points): 3.15271, passed: False
- Counts: non-overlapping 10-bar short blocks: 29, non-overlapping 10-bar blocks (all bars): 70, distinct downward crosses: 2
- Decided by: Rejected: the conditional-minus-unconditional difference is 0 or above, or the falling share on short bars is not above the unconditional share.
- Reading: Blocks are the bars at positions 0,10,20,... of each window with a full 10-bar forward return inside the window, short blocks are those whose bar has forecast < 0, the t-stat is Welch's t between short blocks and all blocks, the main measure is reported in percent, and a downward cross is counted each time the component's raw spread goes from >= 0 to < 0 within a window.
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
