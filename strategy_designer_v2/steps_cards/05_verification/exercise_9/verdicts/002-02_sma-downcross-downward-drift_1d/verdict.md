---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Excess forward 20-bar return of short bars over all bars (non-overlapping 20-bar blocks): -0.00996056; Welch t: -0.222677 (threshold: confirm if excess < 0 with t <= -2 and the supporting slope is not positive; reject if excess > 0 with t >= +2; otherwise inconclusive; at least 6 short blocks (120 short bars))
- Supporting check: Slope of forward 20-bar return on |forecast| within short blocks (should be <= 0): -0.00756711, passed: True
- Counts: non-overlapping 20-bar blocks of short exposure: 20, short bars across all windows: 437, all non-overlapping 20-bar blocks: 34
- Decided by: t lies between -2 and +2, which the plan calls inconclusive.
- Reading: Blocks are the bars at positions 0, 20, 40, ... of each window with a full 20-bar forward return inside the window; a short block is one whose start bar has a negative forecast; the main measure is the Welch t of short-block returns minus all-block returns; the slope uses |forecast| on short blocks; the minimum is not reached if either fewer than 6 short blocks or fewer than 120 short bars.
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
