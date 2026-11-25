---
plan: 032-03_low-volume-decline-continues-more_1d
idea: 032-03_low-volume-decline-continues-more
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: clustered OLS slope of 5-bar excess return on forecast, trending grid cells: 0.000222855; day-clustered OLS t: 0.482832 (threshold: confirm: slope > 0 with t >= 2 (and supporting check); reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: mean negated excess 5-bar return, cells with forecast <= -2: 0.00384856, passed: True
- Counts: regime grid cells: 1616, grid cells with forecast <= -2: 944, days of regime grid cells: 468
- Decided by: The slope's |t| is below 2, which the plan calls inconclusive.
- Reading: Situation bars are those with a negative 28-bar close-to-close return inside the window (the recorded regime where 28 prior bars are not in the window), raw log volume ratio below 0 and a negative forecast; the slope's t uses an OLS with intercept and standard errors clustered by calendar day (UTC); the coin's mean 5-bar return uses all grid cells of all its windows; the plan's 'inconclusive with fewer cases' is reported as 'not observable'.
- Size: unusual move -0.51 % (t -1.17, the cases of one day together: 495 days) per case over 5 bars, -0.043 of the coin's usual move (10.60 %); normal drift in its direction -0.65 %, total -1.17 %; 652 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-03_low-volume-decline-continues-more_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03_low-volume-decline-continues-more_1d`
Measure: `measure.py`
