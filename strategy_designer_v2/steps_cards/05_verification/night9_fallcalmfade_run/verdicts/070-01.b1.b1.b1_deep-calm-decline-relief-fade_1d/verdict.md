---
plan: 070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d
idea: 070-01.b1.b1.b1_deep-calm-decline-relief-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed next-day return minus the coin's mean daily return: 0.00955733; t of the mean, cases pooled by day: 2.8082 (threshold: mean > 0 with t >= 2 to confirm; t <= -2 to reject)
- Supporting check: OLS slope of next-day return on run depth: -0.00429145, passed: True
- Counts: cases: 339, days: 171
- Decided by: Mean short-signed excess return > 0 with t = 2.81 >= 2, negative depth slope, and 339 >= 30 cases.
- Reading: Profile and regime taken from the recorded regime (mean_reversion only arises inside the falling calm profile, whose 365-day percentile cannot be rebuilt from the record), depth from the depth component's last_history_value, cases are mean_reversion bars with nonzero forecast and a next-day close in the same window, the slope uses the raw next-day return with its ordinary OLS t, and the main t clusters cases by UTC day.
- Size: unusual move +0.96 % (t 2.82, the cases of one day together: 171 days) per case over 1 bars, 0.203 of the coin's usual move (5.33 %); normal drift in its direction -0.12 %, total +0.83 %; 339 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004068 on the check folds against +0.009557 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d`
Measure: `measure.py`
