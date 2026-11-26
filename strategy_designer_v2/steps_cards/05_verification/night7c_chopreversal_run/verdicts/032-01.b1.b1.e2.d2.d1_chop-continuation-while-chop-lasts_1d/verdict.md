---
plan: 032-01.b1.b1.e2.d2.d1_chop-continuation-while-chop-lasts_1d
idea: 032-01.b1.b1.e2.d2.d1_chop-continuation-while-chop-lasts
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean signed 7-bar excess return: 0.0175327; t of the weighted mean, cases summed per day: 2.65621 (threshold: confirm: positive with t >= 2 and supporting check > 0; reject: negative with t <= -2)
- Supporting check: upper-half minus lower-half mean signed excess return (split at median |forecast|): 0.0103244, passed: True
- Counts: cases: 1114, days: 366
- Decided by: The weighted mean is positive with t >= 2 and the upper-minus-lower half difference is above 0.
- Reading: The 30-bar efficiency ratio, 7- and 30-bar returns are recomputed from closes inside each window, bars without 30 prior bars in the window are left out of the agreement; a case is a grid bar (positions 0,7,14,... of each window) with non-zero forecast and a 7-bar forward return inside the window, the coin's mean 7-bar return is the mean over all its windows' grid returns, the t is the weighted mean over a day-clustered standard error (weighted deviations summed per day), and the supporting check splits cases into |forecast| above the median versus at or below it, comparing unweighted mean signed excess returns.
- Size: unusual move +1.06 % (t 2.75, the cases of one day together: 1043 days) per case over 7 bars, 0.079 of the coin's usual move (12.44 %); normal drift in its direction -0.03 %, total +1.03 %; 1758 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004321 on the check folds against +0.01753 on every fold
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d2.d1_chop-continuation-while-chop-lasts_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d2.d1_chop-continuation-while-chop-lasts_1d`
Measure: `measure.py`
