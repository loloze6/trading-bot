---
plan: 031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days_1d
idea: 031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-day move of the cases: 0.0125913; t of the mean, cases clustered by day: 1.87585 (threshold: mean above 0 with t >= 2 confirms (with the supporting check); below 0 with t <= -2 rejects)
- Supporting check: top-third minus bottom-third mean unusual move: 0.000541585, passed: True
- Counts: cases: 1920, distinct days: 725
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: A case is the first bet (a forecast rise of at least 2 points from its lowest positive level since the last bet, from 0 after a flat) in each 10-bar grid cell of a window, with its 10-bar return inside the window; the day-clustered t uses the summed deviations per UTC day with a D/(D-1) correction; the top and bottom thirds are the cases with forecast at or above the 2/3 quantile and at or below the 1/3 quantile; the plan's minimum counts lead to 'not observable' as the workflow requires.
- Size: unusual move +1.26 % (t 1.88, the cases of one day together: 725 days) per case over 10 bars, 0.071 of the coin's usual move (15.55 %); normal drift in its direction +1.40 %, total +2.66 %; 1920 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days_1d`
Measure: `measure.py`
