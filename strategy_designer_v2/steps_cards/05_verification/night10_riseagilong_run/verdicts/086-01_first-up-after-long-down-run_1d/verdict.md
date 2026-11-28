---
plan: 086-01_first-up-after-long-down-run_1d
idea: 086-01_first-up-after-long-down-run
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of cases (forecast rise >= 2, one per 5-bar grid cell): -0.00131417; t of the mean, cases of one day taken together: -0.15649 (threshold: confirm: mean > 0 with day-clustered t >= 2 and run-length slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: least-squares slope of unusual moves on run_len: -0.00131434, passed: False
- Counts: cases: 390, distinct days: 262
- Decided by: The t lies between -2 and 2: inconclusive by the plan. No effect (common/verdicts.md): t in the idea's direction -0.156 (below 1), 390 cases (30 needed).
- Reading: Situation recomputed from closes as an up close after >= 2 consecutive down closes (recorded run_len used only where the run reaches the window start), long side, the profile filter left to the regime detector; the plan's 'fewer than 30 cases on 30 days' is reported as not observable; the clustered t uses a D/(D-1) correction so it equals the ordinary t with one case per day; the case's run length is run_len's last_history_value on the case bar.
- Size: unusual move -0.13 % (t -0.16, the cases of one day together: 262 days) per case over 5 bars, -0.030 of the coin's usual move (11.39 %); normal drift in its direction +0.65 %, total +0.52 %; 390 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.156 (below 1), 390 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_riseagilong_run/plans/086-01_first-up-after-long-down-run_1d.md`
Record: `steps_cards/04_backtest/night10_riseagilong_run/backtests/086-01_first-up-after-long-down-run_1d`
Measure: `measure.py`
