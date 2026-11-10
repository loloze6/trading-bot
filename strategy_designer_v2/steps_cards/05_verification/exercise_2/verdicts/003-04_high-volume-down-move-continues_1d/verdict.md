---
plan: 003-04_high-volume-down-move-continues_1d
idea: 003-04_high-volume-down-move-continues
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean next-bar return after active bars minus mean next-bar return over all bars: 0.0002125 (threshold: negative with t <= -2 over at least 60 active bars and negative in at least 4 of 6 windows to confirm; zero or positive to reject)
- Supporting check: slope of next-bar return on forecast across active bars (positive expected): -0.000150546, passed: False
- Cases: 148
- Decided by: Reject: the excess return is zero or positive with at least 60 active bars.
- Reading: Active bars are the bars with a negative forecast. Excess return is pooled across all windows. Its t is (mean of active returns minus the all-bar mean) divided by the standard error of the active returns. A window counts as negative if its own active-minus-all mean is below zero, and a window with no active bars is not negative. The slope regresses the next-bar return on the signed forecast, so a positive slope means larger shorts were followed by larger falls.
Plan: `steps_cards/03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-04_high-volume-down-move-continues_1d`
Measure: `measure.py`
