---
plan: 061-01.b1.b1.b1.d1.d2.d1_upper-half-close-fall-graded_1d
idea: 061-01.b1.b1.b1.d1.d2.d1_upper-half-close-fall-graded
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of short cases, short-signed (signal-bar return minus coin's normal 5-bar drift): 0.0223753; t of the mean, cases summed per day: 2.70431 (threshold: confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2; minimum 30 distinct case days)
- Supporting check: mean unusual move of larger-|forecast| half minus smaller half, > 0: 0.0237484, passed: True
- Counts: distinct case days: 210, cases: 279
- Decided by: mean unusual move positive with t >= 2 and the larger-|forecast| half beating the smaller half: the confirm rule.
- Reading: situation recomputed from prices (fall5's recorded value fills the 5-day return at window starts); a case is the first short bet (rise of |forecast| on the short side of >= 2 from its lowest level since the last bet, reset on flat/long) in each 5-bar grid cell from each window's first row; t clusters cases by UTC day of the signal bar; the larger half is |forecast| strictly above the median, the smaller half at or below it; the 30-day minimum, per the workflow, gives 'not observable'.
- Size: unusual move +2.24 % (t 2.71, the cases of one day together: 210 days) per case over 5 bars, 0.207 of the coin's usual move (11.68 %); normal drift in its direction -0.65 %, total +1.59 %; 279 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01044 on the check folds against +0.02238 on every fold
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d2.d1_upper-half-close-fall-graded_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d2.d1_upper-half-close-fall-graded_1d`
Measure: `measure.py`
