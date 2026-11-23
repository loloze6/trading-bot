---
plan: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d
idea: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed 5-bar unusual move after short signals (before costs): 0.0174715; t of the mean: 1.53703 (threshold: confirm if t >= 2 over at least 20 cases; reject if t <= -2 over at least 20 cases)
- Supporting check: Spearman correlation of thinness with short-signed unusual move > 0: 0.0454732, passed: True
- Counts: cases: 70
- Decided by: The t of the mean short-signed unusual move lies between -2 and 2 over at least 20 cases.
- Reading: A short signal is a fall of the forecast of at least 2 points from its level nearest zero on the short side since the last bet (from 0 after flat), the first one per 5-bar grid cell counted from each window's first row, with the coin's drift the mean of its non-overlapping 5-bar grid returns pooled over all windows.
- Size: unusual move +1.75 % per case over 5 bars, 0.179 of the coin's usual move (10.60 %); normal drift in its direction -0.60 %, total +1.14 %; 70 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d`
Measure: `measure.py`
