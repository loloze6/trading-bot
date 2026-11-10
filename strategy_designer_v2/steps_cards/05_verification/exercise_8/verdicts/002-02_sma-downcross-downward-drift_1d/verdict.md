---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: excess forward 20-bar return on short blocks vs all-bar mean: -0.00996056; one-sample t of mean excess across short blocks: -0.268196 (threshold: confirm if excess < 0 with t <= -2 (slope not positive); reject if excess > 0 with t >= +2; else inconclusive; at least 6 short blocks (120 short bars))
- Supporting check: slope of forward 20-bar return on |forecast| within short blocks (should be <= 0): -0.00756711, passed: True
- Counts: non-overlapping 20-bar blocks of short exposure: 20, short bars across all windows: 437
- Decided by: The t-statistic lies between -2 and +2.
- Reading: Blocks start at positions 0, 20, 40, ... of each window; a short block starts on a bar with a negative forecast; the baseline is the pooled mean forward 20-bar return over all block starts of all windows; the t is the one-sample t of the excess across short blocks; the slope uses |forecast| on short blocks; the minimum requires both 6 blocks and 120 short bars.
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
