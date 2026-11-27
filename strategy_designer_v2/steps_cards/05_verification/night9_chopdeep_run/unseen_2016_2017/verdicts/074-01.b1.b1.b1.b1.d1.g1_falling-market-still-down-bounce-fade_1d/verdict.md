---
plan: 074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 1-day move in the short direction (next-day return minus coin's normal 1-day drift): 0.00171164; t of the mean, cases of one day taken together: 0.232436 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: deeper half minus shallower half of |forecast|, mean unusual move (Welch), above 0 (Welch t 1.827): 0.0259814, passed: True
- Counts: cases: 44, distinct days: 40
- Decided by: The plan's minimum of 100 cases on 60 distinct days is not reached (44 cases on 40 days).
- Reading: Situation = 1-day return > 0, 5-day return < 0 and 60-day return < -10 % (the falling-profile veto), with the recorded regime used where a return cannot be computed inside the window; cases are the workflow's bets (forecast rising on its side by >= 2 points) on every bar of the 1-bar grid; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the deeper half is the top floor(n/2) cases by |forecast| (stable sort), the rest is the shallower half; the plan's 'fewer is inconclusive' is reported as 'not observable' per the workflow; values are fractions.
- Size: unusual move +0.17 % (t 0.24, the cases of one day together: 40 days) per case over 1 bars, 0.028 of the coin's usual move (7.55 %); normal drift in its direction -0.98 %, total -0.81 %; 44 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2016_2017/backtests/074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d`
Measure: `measure.py`
