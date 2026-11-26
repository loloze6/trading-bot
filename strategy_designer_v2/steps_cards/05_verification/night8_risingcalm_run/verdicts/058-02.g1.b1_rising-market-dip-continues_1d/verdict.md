---
plan: 058-02.g1.b1_rising-market-dip-continues_1d
idea: 058-02.g1.b1_rising-market-dip-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 5-bar return on |forecast|: -0.00047797; OLS slope t: -0.80177 (threshold: confirm if slope < 0 with t <= -2; reject if slope > 0 with t >= 2; else inconclusive)
- Supporting check: none
- Counts: grid cases with a nonzero forecast: 917
- Decided by: The slope's t lies between -2 and +2 (inconclusive rule).
- Reading: Situation taken as regime 'unknown' with raw dip < 0 on the short side; the coin's drift is the mean of its 5-bar returns on the non-overlapping grids of all its windows; the plan's minimum of 100 grid cases is applied as a minimum count, so below it the status is 'not observable'.
- Size: unusual move -0.39 % (t -0.74, the cases of one day together: 678 days) per case over 5 bars, -0.039 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -0.99 %; 1273 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/058-02.g1.b1_rising-market-dip-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-02.g1.b1_rising-market-dip-continues_1d`
Measure: `measure.py`
