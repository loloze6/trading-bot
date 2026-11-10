---
plan: 002-03_price-upcross-long-sma-drift_1d
idea: 002-03_price-upcross-long-sma-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope (with intercept) of next-10-bar log return on forecast at block start: 0.00120966; OLS slope t-stat: 0.64857 (threshold: slope t-stat >= 2 confirms (with supporting share higher), <= -2 rejects, between is inconclusive)
- Supporting check: share of positive 10-bar returns in forecast > 0 blocks minus share over all blocks: 0.0042328, passed: True
- Counts: non-overlapping blocks: 70, blocks starting with forecast > 0: 27
- Decided by: Inconclusive: the slope t-stat lies between -2 and 2.
- Reading: The situation 'close above its 200-day SMA' is taken as the component's raw value (debug_info.components.above_sma200.last_history_value) > 0, since warm-up bars are absent and the SMA cannot be rebuilt from prices; blocks start at positions 0, 10, 20, ... of each window, a block needs close[t+10] inside the same window; the supporting check passes when the share of positive returns in forecast > 0 blocks exceeds the share over all blocks; a t-stat >= 2 without the supporting share is not a confirm and is treated as inconclusive.
Plan: `steps_cards/03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-upcross-long-sma-drift_1d`
Measure: `measure.py`
