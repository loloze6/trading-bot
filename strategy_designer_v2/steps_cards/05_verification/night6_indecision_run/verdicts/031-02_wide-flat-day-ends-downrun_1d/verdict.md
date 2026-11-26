---
plan: 031-02_wide-flat-day-ends-downrun_1d
idea: 031-02_wide-flat-day-ends-downrun
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move per long case: -0.00503015; t of the mean, cases of one day clustered: -0.523009 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: none
- Counts: cases: 197, days: 148
- Decided by: The t lies between -2 and 2 over at least 30 cases (inconclusive rule).
- Reading: Situation checked from prices within each window (close below its close 5 bars earlier, range over the 20-bar mean range including the current bar >= 1.0, flatness 1-|close-open|/range >= 0.9, recorded component values used where present), active bars whose 5-bar or 20-bar history lies before the window's first recorded bar left out of the share; a case is the first long bet (forecast rise >= 2 from its lowest long level since the last bet, from 0 after flat) in each 5-bar cell counted from each window's first row, the drift is the coin's mean non-overlapping 5-bar return over all its windows, and the day-clustered standard error sums deviations per UTC day with a G/(G-1) small-sample factor.
- Size: unusual move -0.50 % (t -0.52, the cases of one day together: 148 days) per case over 5 bars, -0.062 of the coin's usual move (10.60 %); normal drift in its direction +0.57 %, total +0.07 %; 197 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02_wide-flat-day-ends-downrun_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02_wide-flat-day-ends-downrun_1d`
Measure: `measure.py`
