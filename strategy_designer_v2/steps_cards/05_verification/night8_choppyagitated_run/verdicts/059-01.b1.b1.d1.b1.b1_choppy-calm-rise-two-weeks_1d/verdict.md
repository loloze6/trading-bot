---
plan: 059-01.b1.b1.d1.b1.b1_choppy-calm-rise-two-weeks_1d
idea: 059-01.b1.b1.d1.b1.b1_choppy-calm-rise-two-weeks
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-removed 14-bar forward return on forecast, grid bars with forecast > 0: 0.00793875; OLS slope t, clustered by day: 2.53421 (threshold: confirm: slope > 0 with t >= 2 (and mean unusual move > 0); reject: slope < 0 with t <= -2)
- Supporting check: mean unusual move of the cases (long side): 0.0098917, passed: True
- Counts: grid cases with forecast > 0: 180, days: 79
- Decided by: The slope is positive with t >= 2 and the mean unusual move is above 0.
- Reading: The profile is the recorded regime 'unknown'; the cases are each window's 0,14,28,... bars with forecast > 0 and a full 14-bar forward return in the window; the coin's mean 14-bar return (its normal drift) is taken over all its windows' grid bars; 'cases of one day taken together' is read as a day-clustered (CR1) standard error of the slope; the plan's 'fewer than 30 cases' rule is applied as the minimum count giving 'not observable'.
- Size: unusual move -0.14 % (t -0.14, the cases of one day together: 375 days) per case over 14 bars, -0.020 of the coin's usual move (18.92 %); normal drift in its direction +2.21 %, total +2.06 %; 581 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004922 on the check folds against +0.007939 on every fold
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1.b1_choppy-calm-rise-two-weeks_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b1_choppy-calm-rise-two-weeks_1d`
Measure: `measure.py`
