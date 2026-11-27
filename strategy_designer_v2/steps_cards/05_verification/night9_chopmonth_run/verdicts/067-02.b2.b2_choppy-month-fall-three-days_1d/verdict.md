---
plan: 067-02.b2.b2_choppy-month-fall-three-days_1d
idea: 067-02.b2.b2_choppy-month-fall-three-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (-forecast/10) x negated excess 3-bar return: 0.00714231; t of the mean, cases of one day summed: 2.26376 (threshold: above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: mean excess 3-bar return, deepest third minus shallowest third: -0.0130902, passed: True
- Counts: grid cases: 1414, distinct days: 503
- Decided by: The main measure is above 0 with t >= 2 and the supporting check passes.
- Reading: The deepest third is the n//3 cases with the most negative forecast and the shallowest the n//3 nearest 0; the coin's mean 3-bar return is over all its grid bars in all windows; the t sums each day's deviations from the mean (clustered standard error with G/(G-1) correction); fewer than the minimum cases is 'not observable'.
- Size: unusual move +0.37 % (t 1.34, the cases of one day together: 824 days) per case over 3 bars, 0.039 of the coin's usual move (9.14 %); normal drift in its direction -0.47 %, total -0.10 %; 1460 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.005313 on the check folds against +0.007142 on every fold
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b2.b2_choppy-month-fall-three-days_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b2.b2_choppy-month-fall-three-days_1d`
Measure: `measure.py`
