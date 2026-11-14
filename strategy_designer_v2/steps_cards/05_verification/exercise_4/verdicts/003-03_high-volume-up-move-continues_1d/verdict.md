---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: position-weighted mean next-bar excess return over coin mean daily return: 0.000313069; t of the weighted mean: 0.110115 (threshold: above 0 with t >= 2 to confirm; <= 0 rejects)
- Supporting check: next-bar return, top third minus bottom third of positions on active bars (Welch t): -0.000546063, passed: False
- Counts: active bars: 151, all bars: 724, bars per third: 50, supporting Welch t: -0.10013
- Decided by: The main measure is positive but the supporting check has the opposite sign, which meets the inconclusive rule.
- Reading: Active bars are forecast > 0 pooled over all windows, weighted by postRebalance_current_allocation (zero-position active bars get zero weight); the benchmark is the mean next-bar return over all bars of all windows pooled; the weighted-mean t is the ordinary t of w_i*x_i/mean(w); thirds are the lowest and highest floor(n/3) positions.
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
