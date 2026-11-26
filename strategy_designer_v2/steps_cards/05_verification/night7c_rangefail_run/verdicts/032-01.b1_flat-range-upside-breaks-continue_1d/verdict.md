---
plan: 032-01.b1_flat-range-upside-breaks-continue_1d
idea: 032-01.b1_flat-range-upside-breaks-continue
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 20-bar move of cases (return minus coin's normal 20-bar drift, signal direction): 0.0677236; t of the mean, cases of one day combined: 1.57061 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean unusual move of cases with forecast above median minus below median: 0.00678774, passed: True
- Counts: cases: 113, days: 101
- Decided by: Inconclusive: t between -2 and 2.
- Reading: Chop is read from the recorded regime and the break from the raw distance > 0 (prices where unrecorded); each 20-bar grid cell keeps its first bet, cases whose 20-bar return leaves the window are dropped, the drift is the coin's mean non-overlapping 20-bar return over all windows, and cases at the median forecast are left out of the supporting check.
- Size: unusual move +6.77 % (t 1.58, the cases of one day together: 101 days) per case over 20 bars, 0.227 of the coin's usual move (21.24 %); normal drift in its direction +2.56 %, total +9.33 %; 113 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-01.b1_flat-range-upside-breaks-continue_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-01.b1_flat-range-upside-breaks-continue_1d`
Measure: `measure.py`
