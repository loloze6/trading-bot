---
plan: 050-01_falling-calm-scaled-week-fall-continuation_1d
idea: 050-01_falling-calm-scaled-week-fall-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 3-bar excess return over the coin's normal drift: 0.00718781; t, cases of one day summed together: 1.59097 (threshold: above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: OLS slope of short excess return on |forecast|, t = 0.659: 0.000267132, passed: False
- Counts: cases: 677, distinct days: 316
- Decided by: The main t lies between -2 and 2 and no reject rule is met: inconclusive.
- Reading: Cases are grid bars 0,3,6,... of each window with forecast < 0 and a full 3-bar return inside the window; the drift is the coin's mean non-overlapping 3-bar return over all its windows; the main t is clustered by UTC day with a G/(G-1) correction; the slope t is the ordinary OLS t; the plan's 30 distinct days is applied as a minimum count.
- Size: unusual move +0.87 % (t 2.01, the cases of one day together: 410 days) per case over 3 bars, 0.099 of the coin's usual move (7.96 %); normal drift in its direction -0.39 %, total +0.48 %; 665 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/050-01_falling-calm-scaled-week-fall-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/050-01_falling-calm-scaled-week-fall-continuation_1d`
Measure: `measure.py`
