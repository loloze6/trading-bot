---
plan: 032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation_1d
idea: 032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 7-bar excess forward return on forecast (grid cases, day-clustered): 0.000970546; slope t (day-clustered): 2.14133 (threshold: confirm: slope > 0 with t >= 2 and supporting check > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean unusual move in signal's direction > 0: 0.00864358, passed: True
- Counts: grid cases: 1889, distinct days: 420
- Decided by: The slope is positive with t >= 2 and the mean unusual move in the signal's direction is above 0.
- Reading: The 30-bar efficiency ratio is recomputed from each window's closes and, on a window's first 30 bars where it cannot be, the recorded regime stands in; the side is the sign of the recorded raw scaled move (7-bar return where missing); the slope's t uses day-clustered standard errors, and the supporting check uses the same grid cases with excess return signed by the forecast.
- Size: unusual move +0.50 % (t 1.32, the cases of one day together: 1091 days) per case over 7 bars, 0.035 of the coin's usual move (12.44 %); normal drift in its direction -0.01 %, total +0.49 %; 2101 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0002274 on the check folds against +0.0009705 on every fold
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation_1d`
Measure: `measure.py`
