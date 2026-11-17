---
plan: 013-06_breakout-volume-drives-continuation_1d
idea: 013-06_breakout-volume-drives-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: high-minus-low relative-volume mean 30-bar excess return: 0.195272; Welch t: 1.65542 (threshold: confirm if positive with Welch t >= 2; reject if negative with Welch t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: kept cases in total: 60, high-volume group: 30, low-volume group: 30
- Decided by: the Welch t lies between -2 and 2, which the plan calls inconclusive
- Reading: the situation is checked as regime 'trending', forecast > 0 and a close above every earlier close of the same window, since the 364 prior closes are not all in the record and windows are never joined; the median is taken over all kept cases pooled across coins and windows, kept bars are chosen greedily in time order within each window, and the coin mean is the mean of the non-overlapping 30-bar returns at window positions 0, 30, 60, ... over all its windows.
Plan: `steps_cards/03_test_plan/volume_run/plans/013-06_breakout-volume-drives-continuation_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/013-06_breakout-volume-drives-continuation_1d`
Measure: `measure.py`
