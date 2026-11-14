---
plan: 002-01_sma-golden-cross-upward-drift_1d
idea: 002-01_sma-golden-cross-upward-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess forward 10-bar return on forecast (non-overlapping, pooled): 0.000202171; OLS slope t: 0.370976 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; else inconclusive)
- Supporting check: share positive fwd 10-bar returns when forecast > 0 minus coin's share positive: -0.0214105, passed: False
- Counts: non-overlapping blocks with forecast > 0: 832, non-overlapping blocks: 1657
- Decided by: The slope's t lies between -2 and 2: inconclusive.
- Reading: Blocks start at positions 0, 10, 20, ... of each window, the forecast is taken at the block's first bar, the coin's holding mean and positive share use the same non-overlapping grid over all its windows, the slope t is the ordinary OLS t, and the supporting check averages, over blocks with forecast > 0, the positive indicator minus that coin's positive share.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-01_sma-golden-cross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-01_sma-golden-cross-upward-drift_1d`
Measure: `measure.py`
