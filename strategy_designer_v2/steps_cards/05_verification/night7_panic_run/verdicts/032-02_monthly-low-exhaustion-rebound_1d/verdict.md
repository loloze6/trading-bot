---
plan: 032-02_monthly-low-exhaustion-rebound_1d
idea: 032-02_monthly-low-exhaustion-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move of the cases (long side), before costs: 0.0219867; t of the mean, cases pooled by day: 1.97277 (threshold: confirm: mean > 0 with t >= 2 and deeper half beats shallower; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, deeper half minus shallower half (median depth split): 0.0387546, passed: True
- Counts: distinct case days: 86, cases: 163
- Decided by: The t lies between -2 and 2.
- Reading: The falling agitated profile is read from the recorded regime (not 'chop', since the detector's trend and volatility components are not recorded and need more history than a window holds), the break from depth.last_history_value or, where missing, recomputed from the window's prior 30 closes; a case is the first bet in each 3-bar grid cell from the window's first row, its unusual move is a fraction (not percent), the t is clustered by UTC day with a D/(D-1) correction, and the median split puts cases strictly below the median depth in the deeper half and the rest in the shallower.
- Size: unusual move +2.20 % (t 1.98, the cases of one day together: 86 days) per case over 3 bars, 0.269 of the coin's usual move (7.96 %); normal drift in its direction +0.39 %, total +2.59 %; 163 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/032-02_monthly-low-exhaustion-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/032-02_monthly-low-exhaustion-rebound_1d`
Measure: `measure.py`
