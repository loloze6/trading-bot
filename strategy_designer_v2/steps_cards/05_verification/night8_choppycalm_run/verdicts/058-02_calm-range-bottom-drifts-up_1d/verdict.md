---
plan: 058-02_calm-range-bottom-drifts-up_1d
idea: 058-02_calm-range-bottom-drifts-up
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 5-bar forward return on forecast (profile bars, non-overlapping grid, pooled): -0.000195073; t of OLS slope: -0.341318 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 5-bar return of grid cases with forecast > 0: -0.00961159, passed: False
- Counts: grid cases with forecast above 0: 281, profile grid cases: 567
- Decided by: The slope's t lies between -2 and 2.
- Reading: Profile bars are bars with regime 'unknown' (the config's only active regime, i.e. choppy calm); the coin's mean 5-bar return is taken on the non-overlapping grid of all its bars over all windows; the regression uses all profile grid cases including forecast 0; the plan's 'fewer than 50 grid cases with forecast above 0' is applied as a minimum count giving 'not observable'.
- Size: unusual move -1.20 % (t -2.78, the cases of one day together: 322 days) per case over 5 bars, -0.132 of the coin's usual move (10.60 %); normal drift in its direction +0.62 %, total -0.58 %; 421 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02_calm-range-bottom-drifts-up_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02_calm-range-bottom-drifts-up_1d`
Measure: `measure.py`
