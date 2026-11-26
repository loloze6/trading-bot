---
plan: 037-01.d1_falling-agitated-rise-giveback_1d
idea: 037-01.d1_falling-agitated-rise-giveback
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess gain per position bar (position x next-day return minus position x coin drift): 0.000513873; t of the mean, cases of one day pooled: 1.60493 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: slope of signal-direction next-day return minus drift on |forecast|: 0.000724515, passed: True
- Counts: cases on the 1-bar grid: 1610, days: 1142, active bars: 1047
- Decided by: The t of the mean excess gain lies between -2 and 2.
- Reading: The falling-agitated profile is taken from the recorded regime (the profile vetoes send every other bar to chop, and its 60/365-bar inputs cannot be rebuilt inside the 120-bar windows) together with the recorded raw rise in (0, 1], expected side short; cases are all bars with a nonzero position on the 1-bar grid, the day-clustered t sums each day's deviations from the mean, and the plan's 'fewer than 100 cases' is reported as not observable.
- Size: unusual move +0.56 % (t 1.99, the cases of one day together: 388 days) per case over 1 bars, 0.121 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.43 %; 651 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/037-01.d1_falling-agitated-rise-giveback_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/037-01.d1_falling-agitated-rise-giveback_1d`
Measure: `measure.py`
