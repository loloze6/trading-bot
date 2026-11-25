---
plan: 032-01.b1.b1.e2.d2.d2_strong-case-chop-continuation_1d
idea: 032-01.b1.b1.e2.d2.d2_strong-case-chop-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-day move over cases, in the forecast's direction: 0.0165404; t of the mean, cases clustered by day: 3.66634 (threshold: confirm: mean > 0 with t >= 2 and top-minus-bottom third > 0; reject: mean < 0 with t <= -2)
- Supporting check: top-third minus bottom-third mean unusual move by abs(forecast): 0.000425326, passed: True
- Counts: cases: 1223, distinct days: 798
- Decided by: The mean unusual move is above 0 with t >= 2 and the top-minus-bottom-third difference is above 0.
- Reading: A case is the first bet (a rise of |forecast| on its side of at least 2 points from its lowest level since the last bet, from 0 after a flat or side change) in each 7-bar cell counted from each window's first row, with the 7-bar return inside the window; the normal drift is the coin's mean 7-bar return on that grid over all windows; t is clustered by UTC day with a G/(G-1) correction; thirds are by sorted abs(forecast) split as evenly as possible; the plan's 'fewer than 30 cases or days' rule is reported as not observable; in the situation check, bars with under 30 bars of window history use the recorded regime for the situation and the 7-day move (or the raw scaled_week sign) for the side.
- Size: unusual move +1.65 % (t 3.67, the cases of one day together: 798 days) per case over 7 bars, 0.119 of the coin's usual move (12.44 %); normal drift in its direction -0.02 %, total +1.63 %; 1223 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.007137 on the check folds against +0.01654 on every fold
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d2.d2_strong-case-chop-continuation_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d2.d2_strong-case-chop-continuation_1d`
Measure: `measure.py`
