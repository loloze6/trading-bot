---
plan: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h
idea: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 78-bar unusual move in the short direction, cases forecast <= -10: 0.0103849; t of the mean: 1.52458 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean unusual move (forecast <= -15) minus (forecast in (-15, -10]): -0.0115568, passed: False
- Counts: cases: 669, cases forecast <= -15: 584, cases forecast between -15 and -10: 85
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Situation = regime 'mean_reversion' (the detector's recorded decision for the flat-prior rule) with the panic raw value > 0 and close[t-6] < close[t-12] where computable, expected side short; a case is the first bar of each 78-bar grid cell (positions 0, 78, ... of each window) with forecast <= -10 whose 78-bar forward return lies inside the window, its forecast at that bar sets the supporting-check group, the normal drift is the coin's mean 78-bar return on the same grid over all its windows, and the plan's 'fewer than 30 cases' minimum is reported as not observable.
- Size: unusual move +1.23 % per case over 78 bars, 0.082 of the coin's usual move (16.89 %); normal drift in its direction -2.01 %, total -0.78 %; 707 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h`
Measure: `measure.py`
