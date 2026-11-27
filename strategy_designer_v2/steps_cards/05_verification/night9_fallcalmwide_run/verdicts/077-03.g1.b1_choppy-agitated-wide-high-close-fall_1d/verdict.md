---
plan: 077-03.g1.b1_choppy-agitated-wide-high-close-fall_1d
idea: 077-03.g1.b1_choppy-agitated-wide-high-close-fall
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move of the short cases over 1 day (next-day return minus coin drift, sign flipped): 0.0077819; t of the mean, cases of one day taken together: 3.16879 (threshold: confirm: mean > 0 with day-clustered t >= 2 (and wider half beats narrower half); reject: mean < 0 with t <= -2)
- Supporting check: wider-half minus narrower-half mean unusual move (split at median |forecast|): 0.00414392, passed: True
- Counts: cases: 533, distinct days: 354
- Decided by: The mean unusual move is above 0 with t >= 2 and the wider half beats the narrower half.
- Reading: The situation is checked as a close in the top quarter of the day's range, (close-low)/(high-low) >= 0.75 from the prices, with a short forecast; the choppy-agitated profile vetoes are not recomputed because their components are not recorded and need more history than a window holds (vetoes only remove bars, they cannot add active bars); cases are short bets (a rise of the short forecast of at least 2 points from its lowest level since the last bet) on every bar, the t clusters deviations by UTC day with a G/(G-1) correction, and the wider half is |forecast| at or above the median, the narrower half below it.
- Size: unusual move +0.78 % (t 3.17, the cases of one day together: 354 days) per case over 1 bars, 0.172 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +0.65 %; 533 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.005718 on the check folds against +0.007782 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-03.g1.b1_choppy-agitated-wide-high-close-fall_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-03.g1.b1_choppy-agitated-wide-high-close-fall_1d`
Measure: `measure.py`
