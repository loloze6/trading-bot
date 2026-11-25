---
plan: 059-01_swing-scaled-rise-continues_1d
idea: 059-01_swing-scaled-rise-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar excess return on forecast: 0.000341715; slope t: 2.0759 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 grid cases)
- Supporting check: none
- Counts: grid cases: 3419
- Decided by: Confirmed on every fold, but the main measure points the other way on the check folds (A, D), the years step 7 does not explore: main measure -0.0001029 on the check folds against +0.0003417 on every fold.
- Reading: All grid bars count as cases, flat forecasts included. Positions 0, 5, 10, ... of each window are used where a 5-bar-ahead close exists. The drift is each coin's mean grid return over all its windows. The t is the ordinary OLS slope t, and fewer than 300 cases is reported as not observable.
- Size: unusual move +0.48 % (t 1.66, the cases of one day together: 1314 days) per case over 5 bars, 0.038 of the coin's usual move (10.60 %); normal drift in its direction -0.02 %, total +0.46 %; 2668 cases
- Direction check on folds A, D (the years step 7 does not explore): disagrees: main measure -0.0001029 on the check folds against +0.0003417 on every fold
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/059-01_swing-scaled-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/059-01_swing-scaled-rise-continues_1d`
Measure: `measure.py`
