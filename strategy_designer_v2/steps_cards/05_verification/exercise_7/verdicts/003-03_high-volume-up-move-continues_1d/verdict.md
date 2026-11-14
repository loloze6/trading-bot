---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: position-weighted mean next-bar excess return: 0.000313069; t of the weighted mean: 0.110115 (threshold: position-weighted mean next-bar excess return > 0 with t >= 2 to confirm; <= 0 to reject)
- Supporting check: next-bar return, top third minus bottom third of positions: -0.000546063, passed: False
- Counts: active bars: 151
- Decided by: The main measure is positive but the supporting check has the opposite sign, which meets the inconclusive rule.
- Reading: The situation is the up_move raw value > 0 (close-to-close change if missing) with volume >= the rolling 20-bar mean volume including the current bar, and active bars lacking 20 bars of volume history are left out of the agreement; the benchmark is the pooled mean of all next-bar returns over the 6 windows; the t of the position-weighted mean is the ordinary t of position*excess/mean(position); the thirds are the pooled active bars ranked by postRebalance_current_allocation (n//3 each); the supporting check is top minus bottom with Welch t.
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
