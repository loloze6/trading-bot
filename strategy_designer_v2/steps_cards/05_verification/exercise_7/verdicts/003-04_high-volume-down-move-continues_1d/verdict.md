---
plan: 003-04_high-volume-down-move-continues_1d
idea: 003-04_high-volume-down-move-continues
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Mean next-bar return after active bars minus mean next-bar return over all bars: 0.0002125; Welch t: 0.0662407 (threshold: Confirm: excess < 0 with t <= -2 over >= 60 active bars and negative in >= 4 of 6 windows; reject: excess >= 0 with >= 60 active bars; otherwise inconclusive)
- Supporting check: OLS slope of next-bar return on signed forecast across active bars (should be > 0): -0.000150546, passed: False
- Counts: active bars: 148, windows with negative excess: 3, windows: 6
- Decided by: Reject: the excess return is zero or positive with at least 60 active bars.
- Reading: Active bars are those with forecast != 0; the baseline is every bar of the same windows (horizon 1, so all bars are on the grid); the t is Welch's between the active and all-bar returns; a window with no active bars does not count as negative; the supporting slope regresses next-bar return on the signed forecast, so a positive slope means a larger short is followed by a larger fall.
Plan: `steps_cards/03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-04_high-volume-down-move-continues_1d`
Measure: `measure.py`
