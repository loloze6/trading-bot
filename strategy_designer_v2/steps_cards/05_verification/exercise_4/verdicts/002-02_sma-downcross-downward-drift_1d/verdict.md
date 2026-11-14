---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 10-bar forward return on short bars minus mean over all bars (%): 0.466185; Welch t: 0.235475 (threshold: difference at most -1.0% per 10 bars with t-stat -2 or lower; 0 or above rejects)
- Supporting check: falling share on short blocks minus falling share on all blocks (points): 3.15271, passed: False
- Counts: non-overlapping 10-bar short blocks: 29, non-overlapping 10-bar blocks, all bars: 70, distinct downward crosses: 2
- Decided by: Rejected: the short-minus-all difference is 0 or above, or the falling share on short bars is not above the unconditional share.
- Reading: Short blocks are grid bars (positions 0,10,20,... of each window with t+10 inside the window) with forecast < 0, compared by Welch t against all grid bars, and a downward cross is counted each time the raw SMA50-SMA200 spread (last_history_value) goes from >= 0 to < 0 inside a window; the minimum counts are checked first, then the reject rule, then the confirm rule.
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
