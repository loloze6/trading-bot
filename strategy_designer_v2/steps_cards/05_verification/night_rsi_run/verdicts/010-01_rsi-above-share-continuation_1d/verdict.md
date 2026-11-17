---
plan: 010-01_rsi-above-share-continuation_1d
idea: 010-01_rsi-above-share-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t-statistic of the slope of next 14-bar excess return on forecast: 1.65376; OLS slope t: 1.65376 (threshold: confirm if t >= +2 with the check passing; reject if t <= -2; otherwise inconclusive)
- Supporting check: mean excess 14-bar return, forecast > 0 minus forecast < 0: 0.0288355, passed: True
- Counts: independent 14-bar samples: 384, samples with forecast > 0: 187, samples with forecast < 0: 186
- Decided by: The slope t-statistic lies between -2 and +2, which the plan calls inconclusive.
- Reading: Situation check uses debug_info.components.rsi_share.last_history_value read as value already centred at 0, expected side long when the share is above one half and short below; the coin's mean 14-bar return is taken over that coin's non-overlapping samples pooled across all its windows, the slope t is the OLS t of excess return on forecast over all pooled samples, and the plan's three-coin count is applied as written to the coins present in the record.
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-01_rsi-above-share-continuation_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-01_rsi-above-share-continuation_1d`
Measure: `measure.py`
