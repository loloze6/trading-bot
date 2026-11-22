---
plan: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound_4h
idea: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move of long cases, pooled over coins: 0.000539467; t of the mean: 0.484616 (threshold: t >= 2 to confirm, t <= -2 to reject, over at least 30 independent cases)
- Supporting check: upper-half minus lower-half mean unusual move (split at median forecast): None, passed: False
- Counts: independent cases: 5709
- Decided by: t is between -2 and 2 over at least 30 independent cases.
- Reading: A case is the first long bet (forecast rise >= 2 from its lowest long level since the last bet) in each 18-bar grid cell of a window, dropped if its 18-bar return leaves the window; the drift is the coin's mean grid 18-bar return over all windows; the upper half is forecast strictly above the median and the lower half the rest.
- Size: unusual move +0.05 % per case over 18 bars, 0.007 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.46 %; 5709 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound_4h`
Measure: `measure.py`
