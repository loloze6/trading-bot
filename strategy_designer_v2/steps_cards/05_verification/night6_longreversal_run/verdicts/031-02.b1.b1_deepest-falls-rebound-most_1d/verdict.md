---
plan: 031-02.b1.b1_deepest-falls-rebound-most_1d
idea: 031-02.b1.b1_deepest-falls-rebound-most
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 30-bar move per bet (return minus coin's normal 30-bar drift, before costs): 0.0360457; t of the mean, clustered by day: 0.990669 (threshold: mean > 0 with day-clustered t >= 2 confirms (with deeper half > shallower half); mean < 0 with t <= -2 rejects)
- Supporting check: mean unusual move of upper half minus lower half, split at median forecast: None, passed: False
- Counts: cases: 145, distinct days: 97
- Decided by: The day-clustered t lies between -2 and 2.
- Reading: A case is the first bet (forecast rise of at least 2 points from its low since the last bet, from 0 at each window start) in each 30-bar grid cell from the window's first row, with its 30-bar forward return inside the window; the upper half is forecasts strictly above the median and the lower half the rest; the clustered t uses the G/(G-1) small-sample factor; fewer than the minimum cases is reported as not observable.
- Size: unusual move +3.60 % (t 1.00, the cases of one day together: 97 days) per case over 30 bars, 0.087 of the coin's usual move (27.67 %); normal drift in its direction +5.16 %, total +8.76 %; 145 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-02.b1.b1_deepest-falls-rebound-most_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b1.b1_deepest-falls-rebound-most_1d`
Measure: `measure.py`
