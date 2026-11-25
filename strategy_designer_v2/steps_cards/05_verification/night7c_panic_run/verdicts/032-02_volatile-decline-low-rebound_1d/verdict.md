---
plan: 032-02_volatile-decline-low-rebound_1d
idea: 032-02_volatile-decline-low-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move after a case (long, minus the coin's normal 5-bar drift): 0.0204635; t of the mean, cases of one day taken together: 0.754605 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: OLS slope of unusual move on forecast: 0.00881108, passed: True
- Counts: cases: 42, days: 27
- Decided by: The t lies between -2 and 2 (or is undefined): inconclusive.
- Reading: Each situation condition is checked only where it can be computed from the window's own bars (the 365-bar range ratio and the 30-bar return cannot be computed early in a window and are then not counted against the bar), the break uses the recorded depth value; a case is the first bet (forecast rise >= 2 from its lowest positive level since the last bet, from 0 after flat) in each 5-bar grid cell of a window, its return runs from that bar's close 5 bars ahead inside the window, the normal drift is the coin's mean non-overlapping 5-bar return over all windows, and the t is day-clustered with a G/(G-1) correction.
- Size: unusual move +2.05 % (t 0.77, the cases of one day together: 27 days) per case over 5 bars, 0.225 of the coin's usual move (10.60 %); normal drift in its direction +0.62 %, total +2.66 %; 42 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02_volatile-decline-low-rebound_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02_volatile-decline-low-rebound_1d`
Measure: `measure.py`
