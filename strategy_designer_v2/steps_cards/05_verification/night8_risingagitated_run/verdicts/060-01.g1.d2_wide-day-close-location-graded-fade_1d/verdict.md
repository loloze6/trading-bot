---
plan: 060-01.g1.d2_wide-day-close-location-graded-fade_1d
idea: 060-01.g1.d2_wide-day-close-location-graded-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess fall (short-signed return minus coin mean daily return) on case bars: 0.00903956; t of the mean, cases of one day taken together: 2.23138 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of excess fall on abs(forecast): 0.00106371, passed: True
- Counts: distinct case days: 236, case bars: 378
- Decided by: Mean excess fall above 0 with t >= 2 and a positive slope on abs(forecast): the confirm rule.
- Reading: Cases are every bar with forecast < 0 (1-bar horizon, so every bar is on the grid), the drift is the coin's mean 1-bar return over all its windows, the day-grouped t sums the deviations per UTC day, the slope is an ordinary least-squares slope required only to be > 0, and the 30-day minimum maps to 'not observable'.
- Size: unusual move +0.95 % (t 2.42, the cases of one day together: 210 days) per case over 1 bars, 0.211 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.82 %; 329 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.005429 on the check folds against +0.00904 on every fold
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2_wide-day-close-location-graded-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1.d2_wide-day-close-location-graded-fade_1d`
Measure: `measure.py`
