---
plan: 031-02.b1_wide-flat-day-continues-uprun_1d
idea: 031-02.b1_wide-flat-day-continues-uprun
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar return of long bets (minus coin's normal 10-bar drift): 0.0191189; t of the mean, cases of one day pooled: 0.922075 (threshold: confirm: mean > 0 with day-pooled t >= 2 and slope on forecast > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of excess 10-bar return on signal forecast: 0.00112322, passed: True
- Counts: cases: 77, distinct days: 68
- Decided by: The day-pooled t is between -2 and 2 (inconclusive rule).
- Reading: Situation recomputed from prices (rise from the recorded prior_rise raw value where present), active bars whose 20-bar range mean cannot be formed inside the window are left out of the agreement; a case is the first long bet (forecast rise >= 2 from its lowest long level since the last bet, from 0 after flat) in each 10-bar grid cell of a window counted from its first row, cases without 10 bars left in the window are dropped, the day-pooled t uses a D/(D-1) correction, and the plan's 'fewer than 30 cases or days' minimum is reported as not observable.
- Size: unusual move +1.91 % (t 0.93, the cases of one day together: 68 days) per case over 10 bars, 0.120 of the coin's usual move (14.49 %); normal drift in its direction +1.22 %, total +3.13 %; 77 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1_wide-flat-day-continues-uprun_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1_wide-flat-day-continues-uprun_1d`
Measure: `measure.py`
