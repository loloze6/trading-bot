---
plan: 062-01_rising-volume-shrink-continues_1d
idea: 062-01_rising-volume-shrink-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 5-bar forward return on forecast, in-profile grid bars, coins pooled: 0.000509456; OLS slope t: 0.871359 (threshold: confirm: slope > 0 with t >= 2 (and supporting difference > 0); reject: slope < 0 with t <= -2)
- Supporting check: mean excess 5-bar return, forecast > 0 minus forecast = 0 (Welch): 0.00919247, passed: True
- Counts: in-profile grid cases: 1345, forecast > 0: 572, forecast = 0: 773
- Decided by: Inconclusive: the slope's t lies between -2 and 2.
- Reading: In-profile grid bars are those where the vol_dryup component is recorded; the normal drift is the coin's mean 5-bar return over the non-overlapping grid of all its windows; the slope's t is the OLS slope over its standard error; the supporting check passes when the difference is above 0, its Welch t being reported.
- Size: unusual move +0.89 % (t 1.34, the cases of one day together: 353 days) per case over 5 bars, 0.077 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +1.48 %; 451 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/062-01_rising-volume-shrink-continues_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/062-01_rising-volume-shrink-continues_1d`
Measure: `measure.py`
