---
plan: N7-01_drift-only-near-high_1d
idea: N7-01_drift-only-near-high
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean forward 5-bar excess return over coin mean: 0.00922003; t of weighted mean (weighted sandwich SE): 2.61176 (threshold: confirm if positive with t >= 2; reject if negative with t <= -2)
- Supporting check: mean forward 5-bar excess return on flat bars with recent high and close below SMA20: -0.00648725, passed: True
- Counts: non-overlapping active 5-bar blocks: 1310, supporting flat blocks: 540
- Decided by: The forecast-weighted mean excess return is positive with t >= 2.
- Reading: Active blocks are grid bars 0,5,10,... of each window with forecast > 0; the coin's mean 5-bar return is over all bars of all its windows; excess on supporting bars is the coin's forward return minus that mean; the weighted t uses SE = sqrt(sum w^2 (x-m)^2)/sum w x sqrt(n/(n-1)); 'new high within 20 bars' means a 20-bar closing high 0-19 bars ago; and fewer than 100 blocks gives 'not observable'.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N7-01_drift-only-near-high_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N7-01_drift-only-near-high_1d`
Measure: `measure.py`
