---
plan: 051-01_falling-agitated-scaled-fall-next-day-rebound_1d
idea: 051-01_falling-agitated-scaled-fall-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move (close[t+1]/close[t]-1 minus coin mean daily return) over bars with forecast > 0: 0.00703452; t of the mean, cases of one day pooled: 3.00734 (threshold: confirm: mean > 0 with t >= 2 and slope > 0 with t >= 2; reject: mean < 0 with t <= -2 or slope < 0 with t <= -2)
- Supporting check: slope of next-day unusual move on forecast (day-pooled t): 0.0010552, passed: True
- Counts: cases: 1468, distinct case days: 702
- Decided by: Confirm: the mean unusual move is above 0 with t >= 2 and the slope is positive with t >= 2.
- Reading: Cases are every bar with forecast > 0 and a next close in the same window, the drift is the coin's mean 1-bar return over all its windows, day pooling uses per-day sums of deviations (mean) or of scores (OLS slope) with a D/(D-1) correction, and the plan's 'fewer than 30 distinct case days' is applied as a minimum count giving 'not observable'.
- Size: unusual move +0.99 % (t 3.34, the cases of one day together: 478 days) per case over 1 bars, 0.212 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +1.12 %; 975 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.002401 on the check folds against +0.007035 on every fold
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/051-01_falling-agitated-scaled-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/051-01_falling-agitated-scaled-fall-next-day-rebound_1d`
Measure: `measure.py`
