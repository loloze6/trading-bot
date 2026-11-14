---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: rejected
---
Evidence:
- Main measure: position-weighted mean next-bar excess return on active bars: -0.000694036 (threshold: above 0 with t >= 2 to confirm; <= 0 rejects)
- Supporting check: next-bar return, top third minus bottom third of positions: -0.000546063, passed: False
- Cases: 151
- Decided by: The position-weighted mean next-bar excess return is <= 0, which rejects.
- Reading: Active bars are forecast > 0 rows with a next close in the same window. Each bar's excess return is its next-bar return minus the mean next-bar return over all bars of its own window. The weighted mean is weighted by postRebalance_current_allocation, with t taken from the per-bar values position*excess/mean(position). Thirds are the n//3 lowest and highest positions among pooled active bars, ranked by stable sort and compared with Welch's t-test.
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
