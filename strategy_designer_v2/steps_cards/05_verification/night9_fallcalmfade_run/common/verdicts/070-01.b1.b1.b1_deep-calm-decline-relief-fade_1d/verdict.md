---
plan: 070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d
idea: 070-01.b1.b1.b1_deep-calm-decline-relief-fade
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed next-day return minus the coin's mean daily return: 0.0075067; t of the mean, cases pooled by day: 2.80312 (threshold: mean > 0 with t >= 2 to confirm; t <= -2 to reject)
- Supporting check: OLS slope of next-day return on run depth: -0.00402682, passed: True
- Counts: cases: 598, days: 253
- Decided by: Mean short-signed excess return > 0 with t = 2.80 >= 2, negative depth slope, and 598 >= 30 cases.
- Reading: Profile and regime taken from the recorded regime (mean_reversion only arises inside the falling calm profile, whose 365-day percentile cannot be rebuilt from the record), depth from the depth component's last_history_value, cases are mean_reversion bars with nonzero forecast and a next-day close in the same window, the slope uses the raw next-day return with its ordinary OLS t, and the main t clusters cases by UTC day.
- Size: unusual move +0.75 % (t 2.81, the cases of one day together: 253 days) per case over 1 bars, 0.158 of the coin's usual move (5.12 %); normal drift in its direction -0.09 %, total +0.66 %; 598 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/common/backtests/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d`
Measure: `measure.py`
