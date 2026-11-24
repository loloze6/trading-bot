---
plan: 031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d
idea: 031-03.b1.b1.e2.e2_raw-scaled-rise-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move per case, long direction: 0.0140093; t of the mean, cases of one day taken together: 0.868401 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: none
- Counts: distinct case days: 41, cases: 68
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet) in each 5-bar grid cell from each window's first row, its 5-bar return inside the window minus the coin's mean non-overlapping 5-bar return over all its windows, with the t's standard error clustered by the signal bar's UTC date (deviations summed per day, D/(D-1) correction), and fewer than 30 days reported as not observable.
- Size: unusual move +1.40 % (t 0.88, the cases of one day together: 41 days) per case over 5 bars, 0.080 of the coin's usual move (9.44 %); normal drift in its direction +0.35 %, total +1.75 %; 68 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2026/backtests/031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d`
Measure: `measure.py`
