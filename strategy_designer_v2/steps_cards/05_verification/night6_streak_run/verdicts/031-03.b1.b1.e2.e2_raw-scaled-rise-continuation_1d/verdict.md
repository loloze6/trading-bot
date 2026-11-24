---
plan: 031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d
idea: 031-03.b1.b1.e2.e2_raw-scaled-rise-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move per case, long direction: 0.0268663; t of the mean, cases of one day taken together: 2.7123 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: none
- Counts: distinct case days: 307, cases: 489
- Decided by: The mean unusual move is above 0 with t >= 2 over at least 30 distinct case days (confirm rule).
- Reading: A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet) in each 5-bar grid cell from each window's first row, its 5-bar return inside the window minus the coin's mean non-overlapping 5-bar return over all its windows, with the t's standard error clustered by the signal bar's UTC date (deviations summed per day, D/(D-1) correction), and fewer than 30 days reported as not observable.
- Size: unusual move +2.69 % (t 2.72, the cases of one day together: 307 days) per case over 5 bars, 0.193 of the coin's usual move (12.45 %); normal drift in its direction +0.78 %, total +3.47 %; 489 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d`
Measure: `measure.py`
