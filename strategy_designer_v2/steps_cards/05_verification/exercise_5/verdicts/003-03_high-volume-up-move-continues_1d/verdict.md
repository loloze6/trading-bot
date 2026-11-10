---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: rejected
---
Evidence:
- Main measure: position-weighted mean next-bar excess return on active bars: -0.000694036; t of the weighted mean: -0.24884 (threshold: above 0 with t >= 2 to confirm; <= 0 rejects)
- Supporting check: next-bar return, top third minus bottom third of positions: -0.000546063, passed: False
- Counts: active bars: 151, windows: 6
- Decided by: Reject: the position-weighted mean next-bar excess return is <= 0.
- Reading: Active bars are forecast > 0 with a next close in the same window, weighted by postRebalance_current_allocation; excess return is the next-bar return minus that window's mean next-bar return over all its bars; the t of the weighted mean is the ordinary t of the values position x excess / mean position (whose mean equals the weighted mean); thirds are the floor(n/3) smallest and largest positions pooled over all windows, compared by Welch t (top minus bottom); the 60-bar minimum is checked before the reject rules.
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
