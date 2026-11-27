---
plan: 074-02.b1.b1.b1_falling-calm-stretch-keeps-falling_1d
idea: 074-02.b1.b1.b1_falling-calm-stretch-keeps-falling
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar short move (fraction): 0.00899231; t of the mean, cases of one day together: 1.83946 (threshold: mean > 0 with day-clustered t >= 2 (and supporting check) to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: deeper half minus shallower half mean unusual short move: -0.000843749, passed: False
- Counts: cases: 1051, distinct days: 508
- Decided by: The t is between -2 and 2, which the plan calls inconclusive.
- Reading: Situation: raw stretch < 0 on short-forecast bars (profile left to the regime); a case is the first short bet (forecast rise of >= 2 points on the short side) in each 5-bar grid cell, with its 5-bar return inside the window; t is the mean over a day-clustered standard error with D/(D-1) correction; halves are the floor(n/2) largest and smallest |forecast| cases, the middle one dropped when n is odd.
- Size: unusual move +0.90 % (t 1.84, the cases of one day together: 508 days) per case over 5 bars, 0.079 of the coin's usual move (11.68 %); normal drift in its direction -0.66 %, total +0.24 %; 1051 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/074-02.b1.b1.b1_falling-calm-stretch-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/074-02.b1.b1.b1_falling-calm-stretch-keeps-falling_1d`
Measure: `measure.py`
