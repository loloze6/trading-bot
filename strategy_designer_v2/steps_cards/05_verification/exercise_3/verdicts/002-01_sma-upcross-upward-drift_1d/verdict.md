---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 10-bar forward return in long blocks minus mean over all blocks: 0.00466185; Welch t: 0.235475 (threshold: excess > 0 with t >= 2 to confirm; excess <= 0 rejects (t <= -2 means reversal))
- Supporting check: long-block hit rate minus all-block hit rate (slope of return on forecast as second view): -0.0315271, passed: False
- Counts: non-overlapping 10-bar long blocks: 29, all non-overlapping 10-bar blocks: 70, windows containing long blocks: 4, windows with positive excess: 0
- Decided by: Inconclusive: excess > 0 but confirm rule not met (t below 2; hit rate not above unconditional; excess positive in only 0 windows (need 4)).
- Reading: Blocks start at rows 0,10,20,... of each window with a full 10-bar return inside it, 'all blocks' includes long ones and the t is Welch's between long and all blocks, per-window excess uses that window's own all-block mean, the slope is fit over all blocks, and 'carried by a single window' means the pooled excess is <= 0 once any one window is left out.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
