---
plan: 003-06_down-move-retrace-by-volume_1d
idea: 003-06_down-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: thin minus heavy mean next-bar give-back share of the drop: -3.14064; Welch t: -0.455078 (threshold: confirm: difference > 0, Welch t >= 2 and thin mean > 0; reject: difference <= 0 with t <= -1; otherwise inconclusive; at least 20 thin and 20 heavy down bars)
- Supporting check: terciles of drop size with the same-sign thin-minus-heavy difference (need >= 2 of 3): 2, passed: True
- Counts: thin down bars: 200, heavy down bars: 124
- Decided by: Inconclusive: a negative difference with Welch t above -1.
- Reading: Volume class uses the 20-bar mean ending at and including the bar, computed inside each window, so bars without 20 bars of volume history are left out of both the situation check and the groups; drop size is close[t]/close[t-1]-1 inside the window; terciles are pooled qcut terciles of |drop| and a tercile 'has the same sign' when its thin-minus-heavy difference shares the sign of the pooled one; since the Inconclusive rule keeps negative differences with t above -1, a negative difference is rejected only with t <= -1 (a zero difference is rejected), and a positive difference with t >= 2 but a thin mean <= 0 is inconclusive.
Plan: `steps_cards/03_test_plan/plans/003-06_down-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-06_down-move-retrace-by-volume_1d`
Measure: `measure.py`
