---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 10-bar forward return on short bars minus mean over all bars (%): 0.466185; Welch t: 0.235475 (threshold: difference at most -1.0% per 10 bars with t-stat of -2 or lower)
- Supporting check: falling share on short blocks minus falling share on all blocks (points): 3.15271, passed: False
- Counts: non-overlapping 10-bar short blocks: 29, non-overlapping 10-bar blocks, all bars: 70, distinct downward crosses: 2
- Decided by: Rejected: the conditional-minus-unconditional 10-bar return difference is 0 or above.
- Reading: Short blocks are grid bars (positions 0,10,20,... per window, return needing t+10 in the same window) with forecast < 0, compared by Welch t against all grid bars pooled over windows; a distinct downward cross is a forecast moving from >= 0 to < 0 inside a window (a window opening already short is not counted); reject rules are checked before confirm after the minimum-count gate.
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
