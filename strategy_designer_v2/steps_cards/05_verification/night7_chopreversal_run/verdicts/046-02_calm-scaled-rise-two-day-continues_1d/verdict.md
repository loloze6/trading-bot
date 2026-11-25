---
plan: 046-02_calm-scaled-rise-two-day-continues_1d
idea: 046-02_calm-scaled-rise-two-day-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 2-bar forward return on forecast (forecast > 0, 2-bar grid): 7.02048e-05; OLS slope t: 0.390977 (threshold: slope t >= 2 confirms (with positive weighted mean); t <= -2 rejects; between is inconclusive)
- Supporting check: forecast-weighted mean excess 2-bar return > 0: 0.00050431, passed: True
- Counts: grid bars with forecast > 0: 2349
- Decided by: The slope's t is between -2 and 2.
- Reading: Situation bars are those with raw scaled_rise > 0 (price return > 0 where the raw value is not recorded) and regime not 'chop' (the calm profile), on the long side (forecast > 0); the coin's mean 2-bar return is the mean over all its windows' 2-bar grid bars, and the slope comes from an OLS with intercept.
- Size: unusual move -0.04 % (t -0.21, the cases of one day together: 1199 days) per case over 2 bars, -0.008 of the coin's usual move (6.58 %); normal drift in its direction +0.25 %, total +0.22 %; 2894 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/046-02_calm-scaled-rise-two-day-continues_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/046-02_calm-scaled-rise-two-day-continues_1d`
Measure: `measure.py`
