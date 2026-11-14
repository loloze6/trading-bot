---
plan: 003-04_high-volume-down-move-continues_1d
idea: 003-04_high-volume-down-move-continues
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean next-bar return after active bars minus mean next-bar return over all bars: 0.0002125; Welch t: 0.0662407 (threshold: excess negative with t <= -2 over at least 60 active bars and negative in at least 4 of 6 windows)
- Supporting check: slope of next-bar return on forecast across active bars (should be positive): -0.000150546, passed: False
- Counts: active bars: 148, all bars: 724, windows with negative excess: 3, windows: 6
- Decided by: Reject: the excess return is zero or positive with at least 60 active bars.
- Reading: Active bars are rows whose regime label is 'trending' (the veto's heavy-volume down-day regime), every bar with a next close in its window counts once as the all-bars baseline, the per-window rule counts windows whose active-minus-all mean is below zero (windows without active bars count as not negative), and 'forecast size' is the signed forecast so a positive slope means larger shorts precede larger falls.
Plan: `steps_cards/03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-04_high-volume-down-move-continues_1d`
Measure: `measure.py`
