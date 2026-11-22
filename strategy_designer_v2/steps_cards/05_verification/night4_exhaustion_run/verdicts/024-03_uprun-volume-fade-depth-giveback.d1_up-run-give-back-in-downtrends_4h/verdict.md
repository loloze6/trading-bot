---
plan: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h
idea: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move of short cases (signed for the short), pooled: 0.00554939; t of the mean: 3.73985 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean unusual move of cases with |forecast| above median minus the others: None, passed: False
- Counts: independent cases: 2891, cases above median |forecast|: 0, cases at or below median |forecast|: 2891
- Decided by: A confirming t (>= 2, positive mean) whose supporting check is not above 0.
- Reading: A case is the first short bet (forecast falling >= 2 points below its highest short level since the last bet, reset at flat or side change) in each 18-bar grid cell counted from each window's first row, the drift is the coin's mean non-overlapping 18-bar return over all its windows, and cases at the median |forecast| go to the smaller group.
- Size: unusual move +0.55 % per case over 18 bars, 0.066 of the coin's usual move (8.17 %); normal drift in its direction -0.41 %, total +0.14 %; 2891 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h`
Measure: `measure.py`
