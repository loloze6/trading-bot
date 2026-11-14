---
plan: 002-03_price-upcross-long-sma-drift_1d
idea: 002-03_price-upcross-long-sma-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-10-bar log return on forecast at block start: 0.00120966; OLS slope t: 0.64857 (threshold: confirm if t >= 2 (with supporting check); reject if t <= -2; else inconclusive)
- Supporting check: share of positive 10-bar returns, forecast > 0 blocks minus all blocks: 0.0042328, passed: True
- Counts: non_overlapping_blocks: 70, blocks_with_forecast_gt_0: 27
- Decided by: Inconclusive: the slope t-stat lies between -2 and 2.
- Reading: Blocks start at positions 0, 10, 20, ... of each window and need close[t+10] inside the window; the t-stat is the OLS slope over its standard error; the supporting check passes when the forecast > 0 share minus the all-blocks share is > 0; t >= 2 with a failed supporting check is read as inconclusive; raw column 'debug_info.components.above_sma200.last_history_value' was used for the situation check since 'ma_dist' was absent.
Plan: `steps_cards/03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-upcross-long-sma-drift_1d`
Measure: `measure.py`
