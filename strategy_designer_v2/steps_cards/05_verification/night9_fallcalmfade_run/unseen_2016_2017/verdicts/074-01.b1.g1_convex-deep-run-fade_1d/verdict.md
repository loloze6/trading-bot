---
plan: 074-01.b1.g1_convex-deep-run-fade_1d
idea: 074-01.b1.g1_convex-deep-run-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: weighted mean next-day short-side excess fall: 0.00923147; t of weighted mean, cases of one day pooled: 1.19593 (threshold: confirm: weighted mean > 0 with t >= 2 over >= 30 case-days and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 case-days)
- Supporting check: deepest third excess per unit depth minus the rest's: -0.0102127, passed: False
- Counts: case-days: 82, cases: 101
- Decided by: The t lies between -2 and 2.
- Reading: Situation rebuilt from prices as an up close right after a down close (the raw depth > 0 on a window's first two bars) with the 60-bar price change below 0 (the recorded regime where 60 bars are not in the window); drift is each coin's mean 1-bar return over all its windows; t is cluster-by-day (weighted deviations summed per day); the deepest third is the top round(n/3) cases by raw depth, compared by unweighted mean excess over mean depth; fewer than 30 case-days is reported as not observable.
- Size: unusual move +0.77 % (t 1.19, the cases of one day together: 27 days) per case over 1 bars, 0.100 of the coin's usual move (7.55 %); normal drift in its direction -0.98 %, total -0.21 %; 30 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.g1_convex-deep-run-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2016_2017/backtests/074-01.b1.g1_convex-deep-run-fade_1d`
Measure: `measure.py`
