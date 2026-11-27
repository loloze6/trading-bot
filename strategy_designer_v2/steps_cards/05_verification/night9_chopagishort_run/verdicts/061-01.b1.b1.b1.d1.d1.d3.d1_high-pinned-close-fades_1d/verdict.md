---
plan: 061-01.b1.b1.b1.d1.d1.d3.d1_high-pinned-close-fades_1d
idea: 061-01.b1.b1.b1.d1.d1.d3.d1_high-pinned-close-fades
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move in the short direction: 0.0233608; t of the mean, cases of one day pooled: 3.46183 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: upper-half minus lower-half mean unusual move (median high_close split): 0.0090826, passed: True
- Counts: cases: 331, distinct days with cases: 249
- Decided by: The mean unusual move is positive with t >= 2 and the upper-minus-lower difference is above 0.
- Reading: Situation computed as r5 (close/close 5 bars before - 1, inside the window) < 0 and close location > 0.5 with the short side, over active bars where both are computable (the profile is a further restriction, not required); a case is the first short bet (rise of |forecast| of at least 2 from its lowest level since the last bet) in each 5-bar grid cell of its window, with a full 5-bar return inside the window; the day-pooled t uses per-day sums of deviations from the mean with a D/(D-1) correction; the supporting split puts cases above the median high_close in the upper half and the rest in the lower half; the plan's minimum of 30 distinct days is applied as 'not observable'.
- Size: unusual move +2.34 % (t 3.47, the cases of one day together: 249 days) per case over 5 bars, 0.209 of the coin's usual move (11.68 %); normal drift in its direction -0.65 %, total +1.69 %; 331 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01394 on the check folds against +0.02336 on every fold
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d1.d3.d1_high-pinned-close-fades_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d1.d3.d1_high-pinned-close-fades_1d`
Measure: `measure.py`
