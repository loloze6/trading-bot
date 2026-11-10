---
plan: 003-04_high-volume-down-move-continues_1d
idea: 003-04_high-volume-down-move-continues
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean next-bar return on active bars minus mean next-bar return on all bars: 0.0002125; Welch t: 0.0662407 (threshold: excess < 0 with t <= -2 over at least 60 active bars, negative in at least 4 of 6 windows)
- Supporting check: slope of next-bar return on signed forecast across active bars (should be positive): -0.000150546, passed: False
- Counts: active bars: 148, all bars: 724, windows with negative excess: 3, windows: 6
- Decided by: The excess return is zero or positive with at least 60 active bars, so the idea is rejected.
- Reading: Active bars are rows with a non-zero, non-missing forecast; the baseline is all bars with a next-bar return in the same windows; the Welch t compares active bars against all bars; per-window excess is active minus all within each window (windows without active bars count as not negative); and the slope regresses next-bar return on the signed forecast so that a positive slope means larger shorts precede larger falls.
Plan: `steps_cards/03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-04_high-volume-down-move-continues_1d`
Measure: `measure.py`
