---
plan: 003-04_high-volume-down-move-continues_1d
idea: 003-04_high-volume-down-move-continues
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean next-bar return on active bars minus mean next-bar return on all bars: 0.0002125 (threshold: negative with t <= -2 over >= 60 active bars and negative in >= 4 of 6 windows)
- Supporting check: slope of next-bar return on signed forecast over active bars (should be positive): -0.000150546, passed: False
- Cases: 148
- Decided by: Reject: the excess return is zero or positive with at least 60 active bars.
- Reading: Active bars are rows whose regime is 'trending' (the veto's heavy-volume down days), pooled across windows against all bars with a next-bar return; t is the excess divided by the active bars' standard error (sd/sqrt(n)); a window counts as negative only if it has active bars and a negative excess; the slope uses the signed forecast so a positive slope means larger shorts precede larger falls; t = 0.070, negative windows = 3.
Plan: `steps_cards/03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-04_high-volume-down-move-continues_1d`
Measure: `measure.py`
