---
plan: 002-01_sma-upcross-upward-drift_1d
idea: 002-01_sma-upcross-upward-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-bar excess return on forecast: -0.00156829; OLS slope t: -0.816674 (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; otherwise inconclusive)
- Supporting check: share of positive excess returns, forecast>0 minus forecast=0: -0.220353, passed: False
- Counts: non-overlapping samples: 70, samples with forecast > 0: 29
- Decided by: Inconclusive rule met: the slope's t lies between -2 and 2 (or could not be computed).
- Reading: The window's mean 10-bar return (holding drift) is the mean of the forward 10-bar return over all bars of that window that have one, samples are taken at positions 0, 10, 20, ... of each window with the full 10 bars inside the window, and the slope's t is the ordinary OLS t (slope / standard error).
Plan: `steps_cards/03_test_plan/plans/002-01_sma-upcross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-upcross-upward-drift_1d`
Measure: `measure.py`
