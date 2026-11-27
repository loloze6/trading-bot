---
plan: 061-01.b1.b1.b1.d1.d1.d3.d2_wide-day-upper-close-fade_1d
idea: 061-01.b1.b1.b1.d1.d1.d3.d2_wide-day-upper-close-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of the short bets (drift removed, short direction): 0.024481; t of the mean, same-day cases together: 3.11547 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: mean unusual move, larger-|forecast| half minus smaller half: 0.0140801, passed: True
- Counts: distinct days carrying cases: 245, cases: 327
- Decided by: The mean unusual move is positive with t >= 2 and the larger half beats the smaller half (confirm rule).
- Reading: Situation = close location >= 0.5 and 5-day close return < 0 from the window's prices with the profile read as the detector's regime not 'chop' (bars whose location or 5-day return cannot be computed are left out); one case per 5-bar grid cell (its first bet, dropped if its 5-bar return leaves the window); the t clusters cases by UTC day (summed deviations, G/(G-1) correction); the larger half is |forecast| above the median and the smaller half at or below it; fewer than 30 days is reported as not observable.
- Size: unusual move +2.45 % (t 3.12, the cases of one day together: 245 days) per case over 5 bars, 0.219 of the coin's usual move (11.68 %); normal drift in its direction -0.65 %, total +1.80 %; 327 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01378 on the check folds against +0.02448 on every fold
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d1.d3.d2_wide-day-upper-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d1.d3.d2_wide-day-upper-close-fade_1d`
Measure: `measure.py`
