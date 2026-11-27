---
plan: 070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d
idea: 070-01.b1.b1.b1_deep-calm-decline-relief-fade
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed next-day return minus the coin's mean daily return: None (threshold: mean > 0 with t >= 2 to confirm; t <= -2 to reject)
- Supporting check: OLS slope of next-day return on run depth: None, passed: None
- Counts: cases: 2
- Decided by: Only 2 cases, fewer than the plan's minimum of 30.
- Reading: Profile and regime taken from the recorded regime (mean_reversion only arises inside the falling calm profile, whose 365-day percentile cannot be rebuilt from the record), depth from the depth component's last_history_value, cases are mean_reversion bars with nonzero forecast and a next-day close in the same window, the slope uses the raw next-day return with its ordinary OLS t, and the main t clusters cases by UTC day.
- Size: unusual move +0.26 % (t 0.49, the cases of one day together: 2 days) per case over 1 bars, 0.039 of the coin's usual move (6.78 %); normal drift in its direction -0.75 %, total -0.48 %; 2 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2016_2017/backtests/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d`
Measure: `measure.py`
