---
plan: 074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d
idea: 074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual next-day move in the short direction on case bars: -0.00287582; t of the mean, cases of one day grouped: -0.820879 (threshold: confirm above 0 with t >= 2 (and check above 0); reject below 0 with t <= -2)
- Supporting check: deeper half minus shallower half of |forecast|, mean unusual move: 0.00329225, passed: True
- Counts: case days: 91, cases: 344, active bars: 519
- Decided by: Only 91 case days, below the plan's minimum of 100 case days.
- Reading: Cases are short-side forecast rises of at least 2 points from the lowest level since the last bet on every bar (1-bar grid), the coin's mean is its mean next-bar return over all its windows, the halves split the cases sorted by |forecast| at n//2 (shallower first, odd case to the deeper half), and the situation check uses r1>0 and r5<0 from closes (profile not recomputed).
- Size: unusual move -0.29 % (t -0.83, the cases of one day together: 91 days) per case over 1 bars, -0.068 of the coin's usual move (3.93 %); normal drift in its direction +0.02 %, total -0.27 %; 344 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2026/backtests/074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d`
Measure: `measure.py`
