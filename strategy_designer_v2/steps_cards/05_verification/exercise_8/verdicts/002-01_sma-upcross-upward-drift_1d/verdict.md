---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of forward 10-bar excess return (minus window mean 10-bar return) on forecast: -0.00156829; OLS slope t: -0.816674 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; else inconclusive; inconclusive if < 40 samples or < 15 with forecast > 0)
- Supporting check: share of positive 10-bar excess returns, forecast > 0 minus forecast = 0: -0.220353, passed: False
- Counts: non-overlapping samples: 70, samples with forecast > 0: 29
- Decided by: Inconclusive: the slope's t lies between -2 and 2.
- Reading: The holding drift is each window's mean forward 10-bar return over all its bars with a valid return, the excess returns are taken on the non-overlapping grid of positions 0, 10, 20, ... of each window, the t is the OLS slope t (with intercept) on the pooled samples, and the supporting check passes when the positive share with forecast > 0 exceeds the share with forecast = 0.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
