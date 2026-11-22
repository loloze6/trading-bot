---
plan: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h
idea: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 78-bar move per long case (return minus coin's normal 78-bar drift): -0.00534129; ordinary t of the mean: -0.805532 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and weighted check > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: forecast-weighted mean unusual move > 0: -0.00177807, passed: False
- Counts: cases: 692
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: The situation is read as bars where the component's raw value is positive (prior 540-bar return and stretch return both negative), the side long; a case is the first bet (forecast rise of >= 2 points from its lowest positive level since the last bet, reset to 0 when flat) in each 78-bar grid cell counted from each window's first row, the normal drift is the mean of the coin's non-overlapping 78-bar returns over all its windows, and cases whose 78-bar return leaves the window are dropped.
- Size: unusual move -0.53 % per case over 78 bars, -0.038 of the coin's usual move (16.89 %); normal drift in its direction +1.98 %, total +1.45 %; 692 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h`
Measure: `measure.py`
