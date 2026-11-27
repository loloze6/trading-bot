---
plan: 074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 1-day move in the short direction (next-day return minus coin's normal 1-day drift): 0.00536366; t of the mean, cases of one day taken together: 2.25361 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: deeper half minus shallower half of |forecast|, mean unusual move (Welch), above 0 (Welch t 3.411): 0.00772512, passed: True
- Counts: cases: 2103, distinct days: 662
- Decided by: The mean unusual move is positive with t >= 2 and the deeper half shows a larger mean than the shallower half.
- Reading: Situation = 1-day return > 0, 5-day return < 0 and 60-day return < -10 % (the falling-profile veto), with the recorded regime used where a return cannot be computed inside the window; cases are the workflow's bets (forecast rising on its side by >= 2 points) on every bar of the 1-bar grid; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the deeper half is the top floor(n/2) cases by |forecast| (stable sort), the rest is the shallower half; the plan's 'fewer is inconclusive' is reported as 'not observable' per the workflow; values are fractions.
- Size: unusual move +0.54 % (t 2.26, the cases of one day together: 662 days) per case over 1 bars, 0.106 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.39 %; 2103 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001416 on the check folds against +0.005364 on every fold
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d`
Measure: `measure.py`
