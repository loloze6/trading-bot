---
plan: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 10-bar forward return on forecast (trending, non-overlapping grid, pooled): 0.00251441; OLS slope t: 3.16689 (threshold: slope t >= 2 confirms (with top-third mean excess > 0), t <= -2 rejects; at least 100 independent cases)
- Supporting check: mean excess 10-bar return of top third of forecasts: 0.0367694, passed: True
- Counts: independent trending-grid cases: 861
- Decided by: The slope's t is 2 or more with at least 100 independent cases and the top-third mean excess return is positive.
- Reading: Situation = 60-bar return > 0 (recomputed from closes inside the window, falling back to the recorded regime where 60 prior bars are not in the window) and RSI above 50 (rsi_mom raw value below 0), long side; the coin's mean 10-bar return is taken on the same non-overlapping grid of all bars of all its windows; the top third is the n//3 grid cases with the highest forecasts (stable sort); fewer than 100 cases is reported as not observable.
- Size: unusual move +0.90 % per case over 10 bars, 0.053 of the coin's usual move (14.49 %); normal drift in its direction +1.16 %, total +2.06 %; 757 cases
Plan: `steps_cards/03_test_plan/validation_run/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d`
Measure: `measure.py`
