---
plan: 031-03.g1.b1.g1_volume-confirmed-two-week-continuation_1d
idea: 031-03.g1.b1.g1_volume-confirmed-two-week-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed 14-bar forward return minus coin's mean 14-bar return, on 14-bar grid: 0.00896619; t of the mean, same-day cases summed: 1.35309 (threshold: mean > 0 with t >= 2 confirms (with both regime means > 0); mean < 0 with t <= -2 rejects; min 100 cases, 30 per regime)
- Supporting check: mean > 0 in both trending and mean_reversion cases: 0.00343977, passed: True
- Counts: cases: 2048, trending cases: 960, mean_reversion cases: 1088, days: 207
- Decided by: t lies between -2 and 2.
- Reading: Cases are assigned to a regime by the recorded regime on the grid bar, the coin's mean is over its 14-bar grid returns in all windows, the t sums same-day deviations into one per day, and the plan's 'too few cases' rule is reported as not observable; supporting-check value is the smaller regime mean.
- Size: unusual move +0.71 % (t 1.21, the cases of one day together: 752 days) per case over 14 bars, 0.034 of the coin's usual move (18.92 %); normal drift in its direction +0.25 %, total +0.96 %; 1989 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.g1_volume-confirmed-two-week-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.g1_volume-confirmed-two-week-continuation_1d`
Measure: `measure.py`
