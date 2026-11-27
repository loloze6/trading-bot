---
plan: 061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded_1d
idea: 061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of short cases (short direction): 0.0211672; t of the mean, cases summed per day: 2.86861 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger |forecast| half minus smaller half: 0.00790458, passed: True
- Counts: cases: 161, distinct days: 130
- Decided by: Confirm rule met: the mean unusual move is above 0 with t >= 2 and the larger-|forecast| half beats the smaller half.
- Reading: A case is the first short bet (a rise of the short forecast of at least 2 points) in each 5-bar grid cell counted from each window's first row; the t uses deviations from the mean summed per UTC day with no small-sample correction; the median split puts |forecast| above the median in the larger half and the rest in the smaller half; the situation check takes r5 from the recorded fall5 raw value and does not re-check the profile.
- Size: unusual move +2.12 % (t 2.87, the cases of one day together: 130 days) per case over 5 bars, 0.182 of the coin's usual move (11.68 %); normal drift in its direction -0.66 %, total +1.46 %; 161 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01276 on the check folds against +0.02117 on every fold
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded_1d`
Measure: `measure.py`
