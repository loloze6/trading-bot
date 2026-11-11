---
plan: 002-05_up-cross-to-reverse-cross-gain_1d
idea: 002-05_up-cross-to-reverse-cross-gain
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 20-bar forward return when forecast > 0 minus mean of all blocks in same coin-windows: -0.0131806; Welch t: -0.645048 (threshold: excess > 0 with t >= 2 confirms; excess < 0 with t <= -2 rejects; otherwise inconclusive)
- Supporting check: hit rate of 20-bar returns when forecast > 0 minus unconditional hit rate: -0.0412321, passed: False
- Counts: non-overlapping 20-bar blocks with forecast > 0: 409, non-overlapping 20-bar blocks in the same coin-windows: 610
- Decided by: The t-statistic lies between -2 and 2, so the result is inconclusive.
- Reading: Blocks start at positions 0, 20, 40, ... of each window with a full 20-bar return inside it; 'the same coin-windows' is read as the coin-windows holding at least one forecast > 0 block, and the excess is tested with Welch's t between the forecast > 0 blocks and all blocks of those windows.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-05_up-cross-to-reverse-cross-gain_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-05_up-cross-to-reverse-cross-gain_1d`
Measure: `measure.py`
