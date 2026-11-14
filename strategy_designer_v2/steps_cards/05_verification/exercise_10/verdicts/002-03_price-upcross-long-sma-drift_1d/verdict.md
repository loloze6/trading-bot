---
plan: 002-03_price-upcross-long-sma-drift_1d
idea: 002-03_price-upcross-long-sma-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope (with intercept) of next-10-bar log return on forecast at block start: 0.00120966; OLS slope t: 0.64857 (threshold: slope t-stat >= 2 confirms (with supporting share higher), <= -2 rejects)
- Supporting check: share of positive 10-bar returns in forecast > 0 blocks minus share over all blocks: 0.0042328, passed: True
- Counts: non-overlapping blocks: 70, blocks starting with forecast > 0: 27
- Decided by: Slope t-stat lies between -2 and 2.
- Reading: The situation is the component's raw value (distance from the 200-day SMA, read from the record's only last_history_value column when 'ma_dist' is absent) above zero with a positive forecast; blocks start at positions 0, 10, 20, ... of each window and are kept only when the bar 10 later is in the same window.
Plan: `steps_cards/03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-upcross-long-sma-drift_1d`
Measure: `measure.py`
