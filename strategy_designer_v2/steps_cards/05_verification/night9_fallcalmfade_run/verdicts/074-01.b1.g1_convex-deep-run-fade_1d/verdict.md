---
plan: 074-01.b1.g1_convex-deep-run-fade_1d
idea: 074-01.b1.g1_convex-deep-run-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: weighted mean next-day short-side excess fall: 0.0150073; t of weighted mean, cases of one day pooled: 4.26308 (threshold: confirm: weighted mean > 0 with t >= 2 over >= 30 case-days and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 case-days)
- Supporting check: deepest third excess per unit depth minus the rest's: 0.00147489, passed: True
- Counts: case-days: 735, cases: 1685
- Decided by: Weighted mean short-side excess fall above 0 with t >= 2 over at least 30 case-days, and the deepest third gains more per unit of depth.
- Reading: Situation rebuilt from prices as an up close right after a down close (the raw depth > 0 on a window's first two bars) with the 60-bar price change below 0 (the recorded regime where 60 bars are not in the window); drift is each coin's mean 1-bar return over all its windows; t is cluster-by-day (weighted deviations summed per day); the deepest third is the top round(n/3) cases by raw depth, compared by unweighted mean excess over mean depth; fewer than 30 case-days is reported as not observable.
- Size: unusual move +1.12 % (t 3.60, the cases of one day together: 319 days) per case over 1 bars, 0.234 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +1.00 %; 608 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.009798 on the check folds against +0.01501 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.g1_convex-deep-run-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.g1_convex-deep-run-fade_1d`
Measure: `measure.py`
