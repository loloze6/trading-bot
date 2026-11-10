---
plan: 003-04_high-volume-down-move-continues_1d
idea: 003-04_high-volume-down-move-continues
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean next-bar return after active bars minus mean next-bar return over all bars: 0.0002125; Welch t: 0.0662407 (threshold: negative with t <= -2 over at least 60 active bars and negative in at least 4 of 6 windows)
- Supporting check: slope of next-bar return on forecast across active bars (should be positive): -0.000150546, passed: False
- Counts: active bars: 148, windows with negative excess return: 3, windows: 6
- Decided by: The excess return is zero or positive with at least 60 active bars, so the idea is rejected.
- Reading: Active bars are rows labelled regime 'trending' with a next bar inside the same window, the baseline is every bar with a next-bar return in the same windows (horizon 1, so every bar is on the grid), the t is Welch's between the two groups, a window without active bars does not count as negative, and the supporting slope regresses next-bar return on the signed forecast so a positive slope means a larger short precedes a larger fall.
Plan: `steps_cards/03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-04_high-volume-down-move-continues_1d`
Measure: `measure.py`
