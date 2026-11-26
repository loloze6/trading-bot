---
plan: 060-02.d2_volume-growth-recent-ten-day-fall_1d
idea: 060-02.d2_volume-growth-recent-ten-day-fall
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next 5-day return minus coin's mean 5-day return on the forecast: 0.0013087; OLS slope t, day-clustered: 2.24255 (threshold: confirm: slope > 0 with t >= 2 on >= 100 cases; reject: slope < 0 with t <= -2 on >= 100 cases)
- Supporting check: none
- Counts: cases: 813, days: 292
- Decided by: Confirm rule: the slope is positive with t >= 2 on at least 100 cases.
- Reading: The situation is the 10-day close-to-close return below 0 computed inside each window (the recorded regime 'mean_reversion' stands in on a window's first 10 bars) and the side is the sign of the raw log volume ratio; the regression has an intercept, its t uses standard errors clustered by calendar day (CR1), the coin's mean 5-day return is taken on the non-overlapping grid of all its windows, and the plan's 100 cases is treated as a minimum count (not observable below it).
- Size: unusual move +1.43 % (t 3.37, the cases of one day together: 574 days) per case over 5 bars, 0.137 of the coin's usual move (10.60 %); normal drift in its direction -0.07 %, total +1.35 %; 828 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.00053 on the check folds against +0.001309 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d2_volume-growth-recent-ten-day-fall_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d2_volume-growth-recent-ten-day-fall_1d`
Measure: `measure.py`
