---
plan: 031-01.g1.g1.g1_two-week-run-carries-weekend_1d
idea: 031-01.g1.g1.g1_two-week-run-carries-weekend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean position-weighted unusual weekend move (forecast/10 x (2-day return - coin mean 2-day return)): 0.00609448; t of the mean, cases of one Friday summed across coins: 2.97011 (threshold: confirm: mean > 0 with t >= 2 over >= 100 distinct Fridays and size check > 0; reject: mean < 0 with t <= -2 over >= 100 distinct Fridays)
- Supporting check: mean unusual move in forecast direction, upper minus lower half of |forecast|: 0.000957351, passed: True
- Counts: distinct Fridays: 410, Friday cases (coin x Friday): 2454
- Decided by: the mean weighted unusual move is above 0 with t >= 2 over at least 100 distinct Fridays, and the size check's difference is above 0.
- Reading: All regime-'trending' bars with a close two bars later in the same window are cases (forecast 0 included, weighing 0), the coin's mean 2-day return is taken on the non-overlapping 0,2,4,... grid of all its windows pooled, and the median split puts |forecast| above the median in the upper half and the rest in the lower half.
- Size: unusual move +0.66 % (t 3.42, the cases of one day together: 409 days) per case over 2 bars, 0.096 of the coin's usual move (6.58 %); normal drift in its direction -0.00 %, total +0.66 %; 2122 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g1_two-week-run-carries-weekend_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g1_two-week-run-carries-weekend_1d`
Measure: `measure.py`
