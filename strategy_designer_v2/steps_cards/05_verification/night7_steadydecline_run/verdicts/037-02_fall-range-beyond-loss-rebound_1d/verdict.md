---
plan: 037-02_fall-range-beyond-loss-rebound_1d
idea: 037-02_fall-range-beyond-loss-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: day-clustered t of the slope of next-day unusual return on forecast (forecast > 0 bars): 0.000420498; day-clustered t of the slope: 3.29992 (threshold: slope t >= 2 with mean unusual move > 0 confirms; slope t <= -2 or mean unusual move t <= -2 rejects)
- Supporting check: mean unusual move > 0 (t 1.516, day-clustered): 0.00157558, passed: True
- Counts: case bars: 8489, distinct days: 2196
- Decided by: Confirm: the slope t is 2 or more and the mean unusual move of the cases is above 0.
- Reading: Cases are all bars with forecast > 0 and a next bar in the same window (horizon 1 bar, so every bar is its own grid cell); the regression is OLS with an intercept and Stata-style day-clustered standard errors; the mean unusual move's t sums the cases' deviations per UTC day.
- Size: unusual move +0.13 % (t 1.09, the cases of one day together: 1727 days) per case over 1 bars, 0.029 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.25 %; 5652 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003456 on the check folds against +0.0004205 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/037-02_fall-range-beyond-loss-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/037-02_fall-range-beyond-loss-rebound_1d`
Measure: `measure.py`
