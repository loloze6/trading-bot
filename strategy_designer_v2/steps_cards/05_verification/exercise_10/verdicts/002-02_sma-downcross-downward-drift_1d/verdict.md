---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: excess forward 20-bar return while short vs all bars: 0.0189852; t of mean excess across non-overlapping short blocks: 0.59476 (threshold: t <= -2 with negative excess (and slope not positive) confirms; t >= +2 with positive excess rejects; else inconclusive)
- Supporting check: slope of fwd 20-bar return on |forecast| within short bars (share of short blocks with negative excess reported in name): -0.00459134, passed: True
- Counts: short blocks: 20, short bars: 437
- Decided by: t lies between -2 and +2 (or is undefined), which the plan calls inconclusive.
- Reading: Blocks are the bars at positions 0, 20, 40, ... of each window with a full 20-bar forward return, the baseline is the mean forward return over all such grid bars of the same window, the t is the ordinary t of the mean excess of short blocks, and the slope uses all short bars with forecast size taken as |forecast|.
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
