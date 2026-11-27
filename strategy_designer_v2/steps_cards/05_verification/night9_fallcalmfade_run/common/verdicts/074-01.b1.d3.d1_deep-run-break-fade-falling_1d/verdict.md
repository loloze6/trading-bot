---
plan: 074-01.b1.d3.d1_deep-run-break-fade-falling_1d
idea: 074-01.b1.d3.d1_deep-run-break-fade-falling
fit: adapted
status: confirmed
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual short-side move, top third of cases by |forecast|: 0.00838109; t of the mean, cases of one day taken together: 2.17375 (threshold: t >= 2 confirms (with top minus bottom > 0), t <= -2 rejects)
- Supporting check: top third minus bottom third mean unusual short-side move: 0.00374114, passed: True
- Counts: cases: 3191, top-third cases: 1064, top-third distinct days: 348, bottom-third cases: 1064
- Decided by: The top-third mean unusual short-side move has t >= 2 and the top-minus-bottom difference is above 0.
- Reading: Situation bars are computed from prices (up close after at least 2 consecutive down closes, and 60-bar percent price change below -10) on active bars where both can be computed inside the window; the top and bottom thirds are the first and last round(n/3) cases sorted by |forecast| (stable order by coin, window, bar); the day-clustered t sums deviations per UTC day; fewer than 30 top-third cases or days is reported as not observable.
- Size: unusual move +0.45 % (t 1.73, the cases of one day together: 574 days) per case over 1 bars, 0.085 of the coin's usual move (5.44 %); normal drift in its direction -0.13 %, total +0.32 %; 1993 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3.d1_deep-run-break-fade-falling_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/common/backtests/074-01.b1.d3.d1_deep-run-break-fade-falling_1d`
Measure: `measure.py`
