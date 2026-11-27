---
plan: 081-01.d1_deep-up-day-five-day-fade_1d
idea: 081-01.d1_deep-up-day-five-day-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move of the short bets, short direction: 0.00714633; t of the mean, cases clustered by day: 2.23861 (threshold: confirm: mean > 0 with t >= 2 and the check passes; reject: mean < 0 with t <= -2)
- Supporting check: deeper-half minus shallower-half mean unusual move (median |forecast| split): 0.00886991, passed: True
- Counts: cases: 5627, distinct days: 1326
- Decided by: The mean unusual move is positive with t >= 2 and the deeper half beats the shallower half.
- Reading: Ret1 is recomputed from closes inside each window (the detector's regime is used on a window's first bar) and 'below the 20-day high' is a raw depth below 0; a case is the first short bet of each 5-bar grid cell (positions 0,5,10,... of each window) with a 5-bar return inside the window, the coin's drift is the mean of its 5-bar grid returns over all its windows, the t clusters cases by UTC day (deviations summed per day, G/(G-1) correction), and the deeper half is the cases with |forecast| above the median, the shallower half those at or below it.
- Size: unusual move +0.71 % (t 2.24, the cases of one day together: 1326 days) per case over 5 bars, 0.056 of the coin's usual move (12.35 %); normal drift in its direction -0.82 %, total -0.11 %; 5627 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003554 on the check folds against +0.007146 on every fold
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/081-01.d1_deep-up-day-five-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/081-01.d1_deep-up-day-five-day-fade_1d`
Measure: `measure.py`
