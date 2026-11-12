---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of forward 10-bar excess return on forecast: -0.00156829; OLS slope t: -0.816674 (threshold: slope positive with t >= 2 confirms; negative with t <= -2 rejects)
- Supporting check: share positive excess (forecast > 0) minus share (forecast = 0): -0.220353, passed: False
- Counts: non-overlapping samples in total: 70, samples with forecast > 0: 29
- Decided by: t = -0.82 lies between -2 and 2.
- Reading: The holding drift is the mean of all overlapping 10-bar forward returns available in each window, samples are bars at positions 0,10,20,... with a full 10-bar return inside the window, the slope t is the ordinary OLS t, and the supporting check passes when the forecast>0 share exceeds the forecast=0 share.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
