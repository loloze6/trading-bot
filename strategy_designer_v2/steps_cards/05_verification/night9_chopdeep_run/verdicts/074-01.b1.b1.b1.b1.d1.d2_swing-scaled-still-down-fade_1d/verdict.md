---
plan: 074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d
idea: 074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual next-day move in the short direction on case bars: 0.00516025; t of the mean, cases of one day grouped: 2.17857 (threshold: confirm above 0 with t >= 2 (and check above 0); reject below 0 with t <= -2)
- Supporting check: deeper half minus shallower half of |forecast|, mean unusual move: 0.0113776, passed: True
- Counts: case days: 671, cases: 2110, active bars: 3099
- Decided by: The main measure is above 0 with t >= 2 and the deeper-minus-shallower check is above 0.
- Reading: Cases are short-side forecast rises of at least 2 points from the lowest level since the last bet on every bar (1-bar grid), the coin's mean is its mean next-bar return over all its windows, the halves split the cases sorted by |forecast| at n//2 (shallower first, odd case to the deeper half), and the situation check uses r1>0 and r5<0 from closes (profile not recomputed).
- Size: unusual move +0.52 % (t 2.18, the cases of one day together: 671 days) per case over 1 bars, 0.102 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.37 %; 2110 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001228 on the check folds against +0.00516 on every fold
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d`
Measure: `measure.py`
