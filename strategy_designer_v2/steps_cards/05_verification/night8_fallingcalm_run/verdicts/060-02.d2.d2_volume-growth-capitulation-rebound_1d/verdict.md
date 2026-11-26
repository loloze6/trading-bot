---
plan: 060-02.d2.d2_volume-growth-capitulation-rebound_1d
idea: 060-02.d2.d2_volume-growth-capitulation-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move of the bets: 0.0172974; t of the mean, cases summed per day: 2.31403 (threshold: positive with t >= 2 (and check passing) confirms; t <= -2 rejects)
- Supporting check: correlation of forecast and unusual 5-day move over in-position grid cells: 0.102143, passed: True
- Counts: cases: 435, distinct days: 308, in-position cells: 469
- Decided by: The mean unusual move is positive with t >= 2 and the forecast/unusual-move correlation is above 0.
- Reading: The situation is checked as recorded log volume ratio > 0 and 10-day return < 0 (recomputed from prices where not recorded), long side, with the falling profile left to the profile code as the Fidelity line states; a case is the first bet (forecast rise >= 2 points from its lowest level on its side since the last bet, from 0 after a flat or side change) in each 5-bar grid cell, its 5-bar return taken from that bet's close; the coin's mean 5-day return uses the 5-bar grid of all its windows; in-position cells are grid bars with a non-zero held allocation; the t is cluster-by-day; the plan's minimum counts (30 cases, 20 days) give 'not observable'.
- Size: unusual move +1.73 % (t 2.32, the cases of one day together: 308 days) per case over 5 bars, 0.168 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +2.32 %; 435 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003458 on the check folds against +0.0173 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d2.d2_volume-growth-capitulation-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d2.d2_volume-growth-capitulation-rebound_1d`
Measure: `measure.py`
