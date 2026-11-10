---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: thin minus heavy mean next-bar share of move: -59.408 (threshold: thin mean below heavy mean with Welch t >= 2.0 and thin mean below 0)
- Supporting check: min over heavy/thin parts of strategy gain minus BTC hold on active bars: -0.131486, passed: False
- Cases: 265
- Decided by: Inconclusive: thin is below heavy but the Welch t-stat is under 2.0.
- Reading: Heavy and thin cases are the bars labelled trending and mean_reversion, the move is close[t]/close[t-1]-1 within the window (first row of a window and non-positive moves excluded), the supporting check compares summed position gains with summed BTC returns on bars with nonzero allocation in each part, and thin<heavy with t>=2 but thin>=0, covered by no rule, is treated as inconclusive.
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
