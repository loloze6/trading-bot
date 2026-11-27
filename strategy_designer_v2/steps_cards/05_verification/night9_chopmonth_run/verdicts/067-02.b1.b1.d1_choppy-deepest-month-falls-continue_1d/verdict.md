---
plan: 067-02.b1.b1.d1_choppy-deepest-month-falls-continue_1d
idea: 067-02.b1.b1.d1_choppy-deepest-month-falls-continue
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-adjusted 7-bar short return, largest third of |forecast|: 0.0269815; t of the mean, clustered by day: 2.59617 (threshold: t >= 2 confirms (with positive convexity), t <= -2 rejects)
- Supporting check: largest-third mean minus smallest-third mean (convexity): 0.0390429, passed: True
- Counts: negative-forecast cases: 631, cases in the largest third: 210, distinct days in the largest third: 103, cases in the smallest third: 210
- Decided by: The main mean has t >= 2 and the largest-minus-smallest third difference is above 0.
- Reading: The 60-day choppy test is recomputed from closes inside each window (the recorded regime 'chop' is used on the first 60 bars where it cannot be); the cases of all coins are pooled and ranked by |forecast| (stable sort), the largest and smallest thirds being the top and bottom floor(n/3) cases; the coin's drift is the mean of its 7-bar returns on all its windows' non-overlapping grids; the day-clustered t sums the deviations per UTC day with a G/(G-1) correction.
- Size: unusual move +1.65 % (t 2.76, the cases of one day together: 503 days) per case over 7 bars, 0.107 of the coin's usual move (14.34 %); normal drift in its direction -1.15 %, total +0.50 %; 772 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01352 on the check folds against +0.02698 on every fold
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b1.b1.d1_choppy-deepest-month-falls-continue_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1.b1.d1_choppy-deepest-month-falls-continue_1d`
Measure: `measure.py`
