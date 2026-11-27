---
plan: 074-01.b1.d3.d1_deep-run-break-fade-falling_1d
idea: 074-01.b1.d3.d1_deep-run-break-fade-falling
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual short-side move, top third of cases by |forecast|: 0.0145805; t of the mean, cases of one day taken together: 1.74257 (threshold: t >= 2 confirms (with top minus bottom > 0), t <= -2 rejects)
- Supporting check: top third minus bottom third mean unusual short-side move: 0.00477108, passed: True
- Counts: cases: 58, top-third cases: 19, top-third distinct days: 18, bottom-third cases: 19
- Decided by: The plan's minimum of 30 top-third cases on at least 30 distinct days is not reached.
- Reading: Situation bars are computed from prices (up close after at least 2 consecutive down closes, and 60-bar percent price change below -10) on active bars where both can be computed inside the window; the top and bottom thirds are the first and last round(n/3) cases sorted by |forecast| (stable order by coin, window, bar); the day-clustered t sums deviations per UTC day; fewer than 30 top-third cases or days is reported as not observable.
- Size: unusual move +0.63 % (t 0.93, the cases of one day together: 26 days) per case over 1 bars, 0.064 of the coin's usual move (7.55 %); normal drift in its direction -0.98 %, total -0.35 %; 28 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3.d1_deep-run-break-fade-falling_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2016_2017/backtests/074-01.b1.d3.d1_deep-run-break-fade-falling_1d`
Measure: `measure.py`
