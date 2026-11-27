---
plan: 067-02.b1.b1.d1.d1_deepest-choppy-falls-three-weeks_1d
idea: 067-02.b1.b1.d1.d1_deepest-choppy-falls-three-weeks
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 21-bar excess return of the deepest fifth of negative-forecast grid cases: 0.0732816; t of the mean, cases summed per day: 1.2487 (threshold: mean above 0 with day-clustered t >= 2 confirms (with check); t <= -2 rejects)
- Supporting check: deepest fifth minus rest, short-direction excess return, Welch t >= 1: 1.9904, passed: True
- Counts: negative-forecast cases: 189, deepest-fifth cases: 38, distinct days among deepest-fifth cases: 22, rest cases: 151
- Decided by: The minimum of 30 distinct days among the deepest-fifth cases is not reached (22).
- Reading: The deepest fifth is the ceil(n/5) negative-forecast grid cases with the most negative forecast (ties broken by day then coin), the normal drift is each coin's mean non-overlapping 21-bar return over all its windows, the supporting Welch t is on individual cases, and fewer than 30 days gives 'not observable'.
- Size: unusual move +3.39 % (t 1.72, the cases of one day together: 297 days) per case over 21 bars, 0.086 of the coin's usual move (29.95 %); normal drift in its direction -4.91 %, total -1.53 %; 427 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b1.b1.d1.d1_deepest-choppy-falls-three-weeks_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1.b1.d1.d1_deepest-choppy-falls-three-weeks_1d`
Measure: `measure.py`
