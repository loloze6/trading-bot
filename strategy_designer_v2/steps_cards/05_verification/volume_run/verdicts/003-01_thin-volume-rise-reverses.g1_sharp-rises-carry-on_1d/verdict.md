---
plan: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on_1d
idea: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of OLS slope of excess 5-bar forward return on up_shock post_pipeline_value (non-overlapping grid): 0.000550479; OLS slope t: 3.43896 (threshold: confirm if slope t >= 2 and supporting check passes; reject if slope t <= -2; otherwise inconclusive)
- Supporting check: mean excess 5-bar return on grid bars with forecast >= 10 is above 0: 0.0119872, passed: True
- Counts: grid cases with forecast above 0: 1660, grid cases with forecast of 10 or more: 662, grid cases in regression: 3419
- Decided by: Slope t is 2 or more and the mean excess return on grid bars with forecast >= 10 is above 0 (confirm rule).
- Reading: The coin's mean 5-bar return is the mean of its grid forward returns pooled over all its windows, the regression is one pooled OLS over all coins' grid bars with the slope t = slope / its standard error, grid bars without a full 5-bar forward return inside the window are dropped, and the plan's 'fewer cases' rule is reported as not observable per the workflow.
- Size: unusual move -0.30 % per case over 5 bars, -0.030 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.29 %; 2976 cases
Plan: `steps_cards/03_test_plan/volume_run/plans/003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on_1d`
Measure: `measure.py`
