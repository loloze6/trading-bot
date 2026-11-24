---
plan: 031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d
idea: 031-03.b1.b1.e2.e1_extreme-scaled-rise-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move per long case: 0.0503845; t of the mean, cases pooled by day: 1.33104 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: mean unusual move, top third by forecast minus bottom third: 0.0512322, passed: True
- Counts: distinct case days: 90, cases: 112
- Decided by: t between -2 and 2, which the plan calls inconclusive.
- Reading: A case is the first long bet (forecast rise of at least 2 points from its lowest long level since the last bet) in each 10-bar grid cell of a window, its return taken from that bar's close 10 bars ahead within the window, the drift is the mean of the coin's grid 10-bar returns over all its windows, and the thirds are floor(n/3) cases at each end of the forecast ranking.
- Size: unusual move +5.04 % (t 1.34, the cases of one day together: 90 days) per case over 10 bars, 0.191 of the coin's usual move (31.94 %); normal drift in its direction +10.26 %, total +15.30 %; 112 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2016_2017/backtests/031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d`
Measure: `measure.py`
