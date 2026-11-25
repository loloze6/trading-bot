---
plan: 032-03.b1.b1_thin-volume-decline-all-coins_1d
idea: 032-03.b1.b1_thin-volume-decline-all-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-day excess return on forecast (day-clustered t): 0.000318729; day-clustered t of slope: 1.02813 (threshold: slope > 0 with t >= 2 confirms (with supporting check); slope < 0 with t <= -2 rejects)
- Supporting check: mean excess 5-day return of cases with forecast < 0 below 0: -0.00575415, passed: True
- Counts: cases: 3610, distinct days: 501
- Decided by: The slope's |t| is below 2.
- Reading: The situation is recomputed as close[t]/close[t-28]-1 < 0 inside each window (active bars with fewer than 28 prior bars in their window are left out of the agreement), the expected side is the sign of the raw log volume ratio (standardise keeps the sign, fall-side short when volume is thin); the coin's normal 5-day drift is the mean of its non-overlapping 5-bar grid returns over all its windows, and the slope's t uses a day-clustered standard error (per-day summed score deviations, with G/(G-1) correction).
- Size: unusual move +0.21 % (t 0.73, the cases of one day together: 1170 days) per case over 5 bars, 0.010 of the coin's usual move (12.04 %); normal drift in its direction -0.26 %, total -0.05 %; 2339 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-03.b1.b1_thin-volume-decline-all-coins_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b1.b1_thin-volume-decline-all-coins_1d`
Measure: `measure.py`
