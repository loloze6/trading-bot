---
plan: 075-01.d2_heavy-volume-fall-two-day-rebound_1d
idea: 075-01.d2_heavy-volume-fall-two-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess 2-bar return on forecast, SE clustered by day: 2.47344; OLS slope t, day-clustered SE: 2.47344 (threshold: confirm if t >= 2 (with top-minus-bottom third > 0); reject if t <= -2)
- Supporting check: mean excess 2-bar return, top third minus bottom third by forecast: 0.00905505, passed: True
- Counts: cases: 9122, distinct days: 1236
- Decided by: The slope's t is 2 or more and the top-minus-bottom-third difference is above 0 (confirm rule).
- Reading: A down day is close below the previous close inside the window (the regime column on a window's first bar), cases are grid bars (positions 0,2,4,... of each window) with a down day, forecast > 0 and a 2-bar return inside the window, the coin's mean is over all its windows' grid 2-bar returns, thirds are the n//3 cases with the largest and smallest forecasts (stable sort), the cluster-robust SE uses the usual G/(G-1)*(N-1)/(N-K) correction, and too few cases or days gives 'not observable' as the workflow requires.
- Size: unusual move +0.09 % (t 0.59, the cases of one day together: 2062 days) per case over 2 bars, 0.016 of the coin's usual move (7.48 %); normal drift in its direction +0.31 %, total +0.40 %; 11587 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +1.969 on the check folds against +2.473 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/075-01.d2_heavy-volume-fall-two-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01.d2_heavy-volume-fall-two-day-rebound_1d`
Measure: `measure.py`
