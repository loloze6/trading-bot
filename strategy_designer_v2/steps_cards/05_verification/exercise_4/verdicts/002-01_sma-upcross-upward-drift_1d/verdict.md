---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 10-bar forward return in long blocks minus mean over all blocks: 0.00466185; Welch t (long blocks vs all blocks): 0.235475 (threshold: excess > 0 with t >= 2 confirms; excess <= 0 rejects (t <= -2 reversal); 0 < t < 2 inconclusive)
- Supporting check: hit rate long blocks minus hit rate all blocks: -0.0315271, passed: False
- Counts: non-overlapping 10-bar long blocks: 29, all non-overlapping 10-bar blocks: 70, windows containing long blocks: 4, windows with positive excess: 0
- Decided by: Inconclusive: positive excess carried by a single window.
- Reading: Blocks start at rows 0,10,20,... of each window with a full 10-bar forward return inside the window, long means forecast > 0 at block start, t is Welch's long-blocks vs all-blocks, each window's excess is its long mean minus its own all-block mean, 'carried by a single window' means dropping some one window makes the pooled excess <= 0, and the slope (over all blocks) is reported only.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
