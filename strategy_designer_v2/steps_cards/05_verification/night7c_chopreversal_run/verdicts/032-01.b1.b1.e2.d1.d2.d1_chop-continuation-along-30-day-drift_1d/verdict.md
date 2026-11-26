---
plan: 032-01.b1.b1.e2.d1.d2.d1_chop-continuation-along-30-day-drift_1d
idea: 032-01.b1.b1.e2.d1.d2.d1_chop-continuation-along-30-day-drift
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed 7-bar unusual move (forward return minus coin's normal drift): 0.0135488; t of the mean, cases of the same day pooled: 2.51666 (threshold: confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, top half minus bottom half of |forecast|: 0.0103244, passed: True
- Counts: cases: 1114, distinct case days: 366
- Decided by: The mean unusual move is positive with t >= 2 and the top half of |forecast| beats the bottom half.
- Reading: Situation computed from closes (30-day efficiency ratio = |close[t]-close[t-30]| / sum of the 30 absolute daily changes, below 0.3, with the 7- and 30-day returns of the same sign, expected side = sign of the 7-day return), active bars lacking 30 bars of in-window history left out of the agreement (2081 such bars); grid = rows 0,7,14,... of each window; normal drift = the coin's mean 7-bar return on that grid over all its windows; t = mean over a day-clustered standard error (deviations summed per day); top/bottom half = the floor(n/2) cases with the largest / smallest |forecast| (middle case dropped when n is odd); fewer than 30 distinct case days is treated as the plan's minimum count (not observable).
- Size: unusual move +1.06 % (t 2.75, the cases of one day together: 1043 days) per case over 7 bars, 0.079 of the coin's usual move (12.44 %); normal drift in its direction -0.03 %, total +1.03 %; 1758 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004318 on the check folds against +0.01355 on every fold
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1.d2.d1_chop-continuation-along-30-day-drift_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1.d2.d1_chop-continuation-along-30-day-drift_1d`
Measure: `measure.py`
