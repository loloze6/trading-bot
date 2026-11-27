---
plan: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 10-bar forward return on forecast (trending, non-overlapping grid, pooled): 0.00312747; OLS slope t: 5.45408 (threshold: slope t >= 2 confirms (with top-third mean excess > 0), t <= -2 rejects; at least 100 independent cases)
- Supporting check: mean excess 10-bar return of top third of forecasts: 0.0451545, passed: True
- Counts: independent trending-grid cases: 2536
- Decided by: The slope's t is 2 or more with at least 100 independent cases and the top-third mean excess return is positive.
- Reading: Situation = 60-bar return > 0 (recomputed from closes inside the window, falling back to the recorded regime where 60 prior bars are not in the window) and RSI above 50 (rsi_mom raw value below 0), long side; the coin's mean 10-bar return is taken on the same non-overlapping grid of all bars of all its windows; the top third is the n//3 grid cases with the highest forecasts (stable sort); fewer than 100 cases is reported as not observable.
- Size: unusual move +1.31 % (t 1.67, the cases of one day together: 985 days) per case over 10 bars, 0.070 of the coin's usual move (16.74 %); normal drift in its direction +1.52 %, total +2.83 %; 2302 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/validation_run/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d`
Measure: `measure.py`
