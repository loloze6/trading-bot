---
plan: 076-01_run-break-three-day-fade_1d
idea: 076-01_run-break-three-day-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: short-signed 3-day return minus normal 3-day drift on run-breaking up days: 0.00339129; t of the mean, cases of one day taken together: 1.60604 (threshold: positive with t >= 2 to confirm; negative with t <= -2 to reject)
- Supporting check: unusual move after 3+ down-day runs minus after 1-day runs (Welch t): 0.0072823, passed: True
- Counts: cases: 4160, cases after runs of 3 or more down days: 971, cases after runs of exactly 1 down day: 2063, days: 1429
- Decided by: inconclusive: t between -2 and 2 on the main measure and no reject rule met
- Reading: Cases are run-breaking up days recomputed from closes (close above prior close after >=1 strict down closes, the recorded run_len raw value used for run length where present), taking the first such day in each 3-bar grid cell from each window's first row with its 3-bar return inside the window, the normal drift being the coin's mean non-overlapping 3-bar return over all its windows, and the t using day-clustered standard errors.
- Size: unusual move +0.34 % (t 1.61, the cases of one day together: 1429 days) per case over 3 bars, 0.044 of the coin's usual move (7.96 %); normal drift in its direction -0.36 %, total -0.02 %; 4160 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/076-01_run-break-three-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/076-01_run-break-three-day-fade_1d`
Measure: `measure.py`
