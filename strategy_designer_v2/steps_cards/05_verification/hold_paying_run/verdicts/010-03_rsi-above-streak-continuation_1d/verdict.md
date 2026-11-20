---
plan: 010-03_rsi-above-streak-continuation_1d
idea: 010-03_rsi-above-streak-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the pooled slope of excess 14-bar forward return on forecast: 1.48446; OLS slope t: 1.48446 (threshold: confirm if t >= 2 (with the check passing), reject if t <= -2)
- Supporting check: timing part of the book's mean daily return before costs > 0: 0.000486504, passed: True
- Counts: grid cases in total: 384, cases with a forecast above 0: 199
- Decided by: The slope's t is 1.48, between -2 and 2.
- Reading: Grid bars at positions 0, 14, 28, ... of each window with a full 14-bar forward return inside it; each coin's mean 14-bar return is the mean over its grid cases across all windows; the slope is one pooled OLS of excess return on forecast with the OLS standard error; the book before costs is the daily mean over coins of position after the trade x next-bar return, and its market part uses each coin's mean daily return over all windows.
Plan: `steps_cards/03_test_plan/hold_paying_run/plans/010-03_rsi-above-streak-continuation_1d.md`
Record: `steps_cards/04_backtest/hold_paying_run/backtests/010-03_rsi-above-streak-continuation_1d`
Measure: `measure.py`
