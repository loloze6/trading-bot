---
plan: 061-01.g1.g3_calm-big-fall-rebounds_1d
idea: 061-01.g1.g3_calm-big-fall-rebounds
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of 10-bar excess forward return on forecast (forecast > 0, grid bars): 0.000668026; OLS slope t (day-summed cases): 0.742625 (threshold: slope t >= 2 confirms (with mean excess > 0); slope t <= -2 rejects)
- Supporting check: mean excess 10-bar return on the same cases above 0: -0.0106677, passed: False
- Counts: independent cases (days): 165, grid bars with forecast > 0: 450, active bars: 4624
- Decided by: Neither rule met: the slope's t is between -2 and 2, or it is 2 or more while the supporting check fails.
- Reading: Grid bars on the same UTC day are summed (both excess return and forecast) into one case before the OLS regression; the coin's mean 10-bar return is the mean over all its windows' grid returns; the mean excess is over grid bars, and its t uses day-summed deviations.
- Size: unusual move -0.17 % (t -0.26, the cases of one day together: 518 days) per case over 10 bars, -0.018 of the coin's usual move (14.49 %); normal drift in its direction +1.29 %, total +1.12 %; 991 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.g3_calm-big-fall-rebounds_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.g3_calm-big-fall-rebounds_1d`
Measure: `measure.py`
