---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 10-bar forward return in long blocks minus mean over all blocks: 0.00466185; Welch t (long blocks vs all blocks): 0.235475 (threshold: excess > 0 with t >= 2 to confirm; excess <= 0 rejects (t <= -2 means reversal))
- Supporting check: hit rate of long blocks minus hit rate of all blocks (long 0.4827586206896552, all 0.5142857142857142; slope of return on forecast: -0.00027366833536417406): -0.0315271, passed: False
- Counts: non-overlapping 10-bar long blocks: 29, non-overlapping 10-bar blocks (all): 70, windows containing long blocks: 4, windows with positive excess: 0
- Decided by: Inconclusive: excess > 0 but t between 0 and 2.
- Reading: Blocks start at rows 0, 10, 20, ... of each window with returns kept inside the window; long means forecast > 0 at the block start; the t is Welch's long-blocks vs all-blocks; per-window excess is the window's long mean minus its all-block mean; 'carried by a single window' means the pooled excess drops to <= 0 when any one window is removed; the forecast-slope view is reported but does not enter the decision since the confirm rule omits it.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
