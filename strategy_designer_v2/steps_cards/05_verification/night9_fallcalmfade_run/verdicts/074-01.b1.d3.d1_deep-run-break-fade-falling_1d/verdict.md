---
plan: 074-01.b1.d3.d1_deep-run-break-fade-falling_1d
idea: 074-01.b1.d3.d1_deep-run-break-fade-falling
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual short-side move, top third of cases by |forecast|: 0.0169397; t of the mean, cases of one day taken together: 3.73605 (threshold: t >= 2 confirms (with top minus bottom > 0), t <= -2 rejects)
- Supporting check: top third minus bottom third mean unusual short-side move: 0.0135196, passed: True
- Counts: cases: 834, top-third cases: 278, top-third distinct days: 163, bottom-third cases: 278
- Decided by: The top-third mean unusual short-side move has t >= 2 and the top-minus-bottom difference is above 0.
- Reading: Situation bars are computed from prices (up close after at least 2 consecutive down closes, and 60-bar percent price change below -10) on active bars where both can be computed inside the window; the top and bottom thirds are the first and last round(n/3) cases sorted by |forecast| (stable order by coin, window, bar); the day-clustered t sums deviations per UTC day; fewer than 30 top-third cases or days is reported as not observable.
- Size: unusual move +1.28 % (t 3.96, the cases of one day together: 276 days) per case over 1 bars, 0.265 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +1.16 %; 506 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01361 on the check folds against +0.01694 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3.d1_deep-run-break-fade-falling_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d3.d1_deep-run-break-fade-falling_1d`
Measure: `measure.py`
