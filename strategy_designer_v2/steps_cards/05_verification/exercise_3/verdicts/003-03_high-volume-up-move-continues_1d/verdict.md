---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: rejected
---
Evidence:
- Main measure: position-weighted mean next-bar excess return on active bars: -0.000694036; t of the mean of position x excess return: -0.24884 (threshold: above 0 with t >= 2 to confirm; <= 0 rejects)
- Supporting check: next-bar return, top third minus bottom third of positions (Welch t -0.100): -0.000546063, passed: False
- Counts: active bars: 151, bars per third: 50
- Decided by: The position-weighted mean next-bar excess return is <= 0.
- Reading: Active bars are rows with forecast > 0 and a next close in the same window, the weight is postRebalance_current_allocation, excess is the next-bar return minus the mean next-bar return of all bars of that same window, the weighted mean is sum(pos*excess)/sum(pos) with its t taken as the ordinary t of the per-bar pos*excess values, and the thirds are the floor(n/3) lowest and highest positions compared by Welch t (top minus bottom).
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
