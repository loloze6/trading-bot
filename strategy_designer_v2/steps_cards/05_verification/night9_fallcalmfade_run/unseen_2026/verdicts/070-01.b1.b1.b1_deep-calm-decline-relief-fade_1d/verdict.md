---
plan: 070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d
idea: 070-01.b1.b1.b1_deep-calm-decline-relief-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed next-day return minus the coin's mean daily return: -0.000793319; t of the mean, cases pooled by day: -0.135569 (threshold: mean > 0 with t >= 2 to confirm; t <= -2 to reject)
- Supporting check: OLS slope of next-day return on run depth: -0.00201878, passed: True
- Counts: cases: 105, days: 38
- Decided by: Main t = -0.14 lies between -2 and 2 and no reject rule is met.
- Reading: Profile and regime taken from the recorded regime (mean_reversion only arises inside the falling calm profile, whose 365-day percentile cannot be rebuilt from the record), depth from the depth component's last_history_value, cases are mean_reversion bars with nonzero forecast and a next-day close in the same window, the slope uses the raw next-day return with its ordinary OLS t, and the main t clusters cases by UTC day.
- Size: unusual move -0.08 % (t -0.14, the cases of one day together: 38 days) per case over 1 bars, -0.012 of the coin's usual move (3.93 %); normal drift in its direction +0.03 %, total -0.05 %; 105 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2026/backtests/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d`
Measure: `measure.py`
