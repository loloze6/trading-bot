---
plan: 058-02.g1_choppy-agitated-dip-continues_1d
idea: 058-02.g1_choppy-agitated-dip-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted next-5-bar return on the forecast, profile bars, 5-bar grid, coins pooled: 0.000259205; regression t: 0.317578 (threshold: confirm if t >= +2 (with deepest third below 0); reject if t <= -2; at least 30 non-zero grid cases)
- Supporting check: mean drift-adjusted 5-bar return of the deepest third of the forecast: -0.0144363, passed: True
- Counts: grid cases inside the profile with a non-zero forecast: 174, grid cases inside the profile: 244
- Decided by: The slope's t lies between -2 and +2.
- Reading: The profile is the bars whose regime is not 'chop'. The regression uses every profile grid bar, including those with a zero forecast. The drift is the coin's mean 5-bar grid return over all its bars. The deepest third is the floor(n/3) most negative of the non-zero-forecast profile grid cases. The situation side uses last_history_value, or the price-based 5-bar distance where that value is missing.
- Size: unusual move +0.29 % (t 0.55, the cases of one day together: 276 days) per case over 5 bars, 0.038 of the coin's usual move (10.60 %); normal drift in its direction -0.64 %, total -0.36 %; 337 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/058-02.g1_choppy-agitated-dip-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-02.g1_choppy-agitated-dip-continues_1d`
Measure: `measure.py`
