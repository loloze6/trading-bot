---
plan: 031-03.b1.b1_up-streak-continuation-in-uptrend_1d
idea: 031-03.b1.b1_up-streak-continuation-in-uptrend
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move after long bets (forecast rise >= 2 points, once per 5-bar cell): 0.00377157; t of the mean, cases clustered by day: 1.03797 (threshold: confirm: mean > 0 with day-clustered t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on forecast: 0.000898691, passed: True
- Counts: cases: 3360, distinct days: 1136
- Decided by: t between -2 and 2: inconclusive rule.
- Reading: Situation = 30-day close return > 0 (detector's regime on a window's first 30 bars) and the bar closed up with a positive streak raw value, side long; a case is the first bet in each 5-bar grid cell of its window (bet = forecast rise >= 2 from its lowest positive level since the last bet, reset at flat), its forecast is the forecast on that bar, the drift is the coin's mean non-overlapping 5-bar return over all its windows, and the t clusters cases by UTC calendar day with a G/(G-1) factor.
- Size: unusual move +0.38 % (t 1.04, the cases of one day together: 1136 days) per case over 5 bars, 0.026 of the coin's usual move (11.58 %); normal drift in its direction +0.75 %, total +1.12 %; 3360 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1_up-streak-continuation-in-uptrend_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1.b1_up-streak-continuation-in-uptrend_1d`
Measure: `measure.py`
