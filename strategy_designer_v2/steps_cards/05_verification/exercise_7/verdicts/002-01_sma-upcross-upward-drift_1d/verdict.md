---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar forward return in long blocks minus mean over all blocks: 0.00466185; Welch t (long blocks vs all blocks): 0.235475 (threshold: excess > 0 with t >= 2 confirms; excess <= 0 rejects (t <= -2 = reversal))
- Supporting check: hit rate of long blocks minus hit rate of all blocks: -0.0315271, passed: False
- Counts: non-overlapping 10-bar long blocks: 29, windows containing long blocks: 4, windows with positive excess: 0, all blocks: 70
- Decided by: Inconclusive: the excess is > 0 but with t between 0 and 2.
- Reading: Blocks start at positions 0, 10, 20, ... of each window with the forward return inside the window, long blocks have forecast > 0 at the start, t is Welch's t of long-block returns against all-block returns, each window's excess uses that window's own all-block mean, the slope is fitted over all blocks, and 'carried by a single window' means that dropping any one window leaves a pooled excess <= 0.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
