---
plan: 058-01_calm-downtrend-depth-continues_1d
idea: 058-01_calm-downtrend-depth-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean signed 5-bar excess return (short side): 0.00290122; t of the weighted mean, cases of one day pooled: 0.373081 (threshold: confirm above 0 with t >= 2 and the supporting check above 0; reject below 0 with t <= -2)
- Supporting check: larger-|forecast| half minus smaller-|forecast| half signed excess return: -0.000460064, passed: False
- Counts: grid cases in a position (forecast < 0): 475, days: 201
- Decided by: The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive.
- Reading: The falling calm profile is read from the recorded regime (not 'chop'); halves are split by rank of |forecast| (middle case left out when odd) and compared by their unweighted mean; the day-pooled t sums the weighted deviations per UTC day (cluster-robust, J/(J-1) correction); the plan's 'fewer than 30 grid cases' minimum is reported as not observable.
- Size: unusual move +0.74 % (t 1.16, the cases of one day together: 321 days) per case over 5 bars, 0.067 of the coin's usual move (10.60 %); normal drift in its direction -0.65 %, total +0.09 %; 469 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-01_calm-downtrend-depth-continues_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01_calm-downtrend-depth-continues_1d`
Measure: `measure.py`
