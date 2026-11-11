---
plan: 002-01_sma-golden-cross-upward-drift_1d
idea: 002-01_sma-golden-cross-upward-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess forward 10-bar return on forecast (non-overlapping, pooled): 0.000223776; OLS t of slope: 0.410585 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; otherwise inconclusive; inconclusive if fewer than 100 non-overlapping blocks with forecast > 0)
- Supporting check: share of positive fwd 10-bar returns on forecast>0 bars minus coin's share over all bars: -0.0176805, passed: False
- Counts: non-overlapping blocks with forecast > 0: 832, non-overlapping blocks: 1657
- Decided by: The slope's t lies between -2 and 2: inconclusive.
- Reading: The coin's holding mean and positive share use all overlapping 10-bar returns of all its windows, the regression is OLS with intercept on grid bars 0,10,20,... of each window, and the supporting check pools all forecast>0 bars, each compared with its own coin's share.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-01_sma-golden-cross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-01_sma-golden-cross-upward-drift_1d`
Measure: `measure.py`
