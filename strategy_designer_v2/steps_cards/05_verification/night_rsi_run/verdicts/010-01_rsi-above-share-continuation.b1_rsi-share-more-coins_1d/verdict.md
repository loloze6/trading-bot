---
plan: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d
idea: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t-statistic of the slope of 14-bar excess forward return on forecast (pooled, non-overlapping): -0.299209; OLS slope t: -0.299209 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: non-overlapping cases with a recorded forecast: 1152
- Decided by: t = -0.30 lies between -2 and +2 over 1152 cases.
- Reading: Grid at positions 0, 14, 28, ... of each window, keeping only bars with a bar 14 rows later in the same window. Each coin's mean 14-bar return is the mean over all of its grid returns in all windows. OLS with an intercept and its usual slope t. The plan's 'fewer than 200 cases' minimum is treated as 'not observable'. Active bars with a missing or zero raw value count as disagreeing in the situation check.
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d`
Measure: `measure.py`
