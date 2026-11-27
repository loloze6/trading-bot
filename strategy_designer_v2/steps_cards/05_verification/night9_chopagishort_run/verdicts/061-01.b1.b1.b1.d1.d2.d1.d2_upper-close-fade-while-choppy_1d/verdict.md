---
plan: 061-01.b1.b1.b1.d1.d2.d1.d2_upper-close-fade-while-choppy_1d
idea: 061-01.b1.b1.b1.d1.d2.d1.d2_upper-close-fade-while-choppy
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move per short case, in the short direction, before costs: 0.0223753; t of the mean, cases of one day taken together: 2.70431 (threshold: t of the unusual move >= 2 (with supporting correlation > 0) confirms; t <= -2 rejects)
- Supporting check: correlation of forecast and next 5-bar return on grid bars with forecast < 0: 0.148442, passed: True
- Counts: cases: 279, distinct days: 210, supporting grid bars: 85
- Decided by: the unusual move's t is 2 or more and the supporting correlation is above 0
- Reading: the profile is read from the regime column (not 'chop'), a case is the first short bet (forecast magnitude rising >= 2 from its lowest short level since the last bet) in each 5-bar grid cell of a window, the drift is the coin's mean non-overlapping 5-bar return over all its windows, the t uses day-clustered deviations, and the plan's 'fewer than 30 cases or 20 days' is applied as the minimum counts (not observable)
- Size: unusual move +2.24 % (t 2.71, the cases of one day together: 210 days) per case over 5 bars, 0.207 of the coin's usual move (11.68 %); normal drift in its direction -0.65 %, total +1.59 %; 279 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01044 on the check folds against +0.02238 on every fold
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d2.d1.d2_upper-close-fade-while-choppy_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d2.d1.d2_upper-close-fade-while-choppy_1d`
Measure: `measure.py`
