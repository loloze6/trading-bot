---
plan: 032-03.b2.b2_deep-calm-decline-five-days_1d
idea: 032-03.b2.b2_deep-calm-decline-five-days
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean across days of the |forecast|/10-weighted short-direction unusual 5-bar move: 0.0111757; t of the mean across days: 0.880342 (threshold: confirm t >= 2 with slope > 0; reject t <= -2; at least 30 distinct case days)
- Supporting check: OLS slope of short-direction unusual 5-bar move on |forecast|: 0.000486947, passed: True
- Counts: distinct case days: 380, cases: 1080
- Decided by: Main-measure t between -2 and 2 (inconclusive rule).
- Reading: The coin's mean 5-bar return is taken on the non-overlapping 5-bar grid of all its windows, the slope is unweighted over all cases, a case day is the UTC date of the case bar, and the volume regime is recomputed from volume where a window holds 118 bars, else read from the recorded regime.
- Size: unusual move +0.30 % (t 0.68, the cases of one day together: 544 days) per case over 5 bars, 0.027 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -0.29 %; 912 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-03.b2.b2_deep-calm-decline-five-days_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b2.b2_deep-calm-decline-five-days_1d`
Measure: `measure.py`
