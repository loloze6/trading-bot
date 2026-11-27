---
plan: 067-01.b1.g1.b1.d1_choppy-deep-month-slide-continues_1d
idea: 067-01.b1.g1.b1.d1_choppy-deep-month-slide-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed unusual 10-bar move of short bets (minus coin drift, x -1): 0.0181959; t of the mean, cases summed per day: 2.40841 (threshold: t >= 2 with positive mean confirms (with check); t <= -2 with negative mean rejects)
- Supporting check: largest-forecast third minus smallest third of signed unusual move: 0.0268596, passed: True
- Counts: distinct days with cases: 425, cases: 636
- Decided by: Mean signed unusual move positive with t >= 2 and largest third minus smallest third > 0.
- Reading: The 60-day return is recomputed from closes inside the window (recorded regime used where 60 prior bars are not in the window) and the 30-day fall is the recorded fall30 raw value < 0; a bet is a rise of the short forecast's size of >= 2 points from its lowest level since the last bet (reset at flat), the first bet in each 10-bar grid cell of a window is the case, drift is the coin's mean 10-bar grid return over all its windows, the t clusters cases by UTC day with a G/(G-1) correction, thirds are equal splits of cases sorted by |forecast|, and fewer than 30 distinct days gives 'not observable'.
- Size: unusual move +1.82 % (t 2.41, the cases of one day together: 425 days) per case over 10 bars, 0.100 of the coin's usual move (16.82 %); normal drift in its direction -1.49 %, total +0.33 %; 636 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.009682 on the check folds against +0.0182 on every fold
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1.d1_choppy-deep-month-slide-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.d1_choppy-deep-month-slide-continues_1d`
Measure: `measure.py`
