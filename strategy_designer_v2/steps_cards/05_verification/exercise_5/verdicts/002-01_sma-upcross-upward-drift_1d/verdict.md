---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 10-bar forward return in long blocks minus mean over all blocks: 0.00466185; Welch t (long blocks vs all blocks): 0.235475 (threshold: excess > 0 with t >= 2 confirms; excess <= 0 rejects (t <= -2 means reversal); 0 < t < 2 inconclusive)
- Supporting check: long-block hit rate minus unconditional hit rate (slope of 10-bar return on forecast: 0.000401887): -0.0315271, passed: False
- Counts: non-overlapping 10-bar long blocks: 29, non-overlapping 10-bar blocks (all): 70, windows containing long blocks: 4, windows with positive excess: 0
- Decided by: Inconclusive: the excess is > 0 but t is between 0 and 2.
- Reading: Blocks start at rows 0, 10, 20, ... of each window with the return kept only when close[t+10] lies in the same window, a long block is one whose forecast at the block start is > 0, the per-window excess is that window's long-block mean minus that window's all-block mean, 'carried by a single window' is read as only one window having a positive excess, and the forecast-size slope is fit over all blocks with a forecast and reported but does not enter the decision.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
