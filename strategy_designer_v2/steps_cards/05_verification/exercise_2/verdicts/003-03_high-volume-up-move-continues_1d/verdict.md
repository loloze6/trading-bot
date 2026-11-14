---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: rejected
---
Evidence:
- Main measure: position-weighted mean next-bar excess return on active bars: -0.000694036 (threshold: above 0 with t >= 2 to confirm; <= 0 rejects)
- Supporting check: top-third minus bottom-third positions mean next-bar return: -0.000546063, passed: False
- Cases: 151
- Decided by: The position-weighted mean next-bar excess return is <= 0, which meets the reject rule.
- Reading: Active bars are forecast > 0 with the position taken as postRebalance_current_allocation; excess is the next-bar return minus that window's mean next-bar return over all its bars; the weighted mean's t uses a heteroskedasticity-robust weighted standard error pooled over all windows; thirds are n//3 active bars ranked by position, compared on raw next-bar return with a Welch t-test; and the 60-bar minimum is checked before the other rules.
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
