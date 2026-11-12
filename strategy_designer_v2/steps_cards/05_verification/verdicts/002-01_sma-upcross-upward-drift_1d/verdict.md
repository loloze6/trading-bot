---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of forward 10-bar excess return (vs window mean 10-bar return) on forecast: -0.00178248; OLS slope t: -0.930143 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; else inconclusive)
- Supporting check: share of positive excess returns, forecast > 0 minus forecast = 0: -0.254836, passed: False
- Counts: non-overlapping samples: 70, samples with forecast > 0: 29
- Decided by: Inconclusive: the slope's t lies between -2 and 2.
- Reading: Samples are the bars at positions 0, 10, 20, ... of each window with a full 10-bar forward return inside the window, the holding drift is the mean of those same non-overlapping 10-bar returns in that window, the slope's t is the ordinary OLS slope / standard error, and the supporting check passes when the forecast > 0 share exceeds the forecast = 0 share.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
