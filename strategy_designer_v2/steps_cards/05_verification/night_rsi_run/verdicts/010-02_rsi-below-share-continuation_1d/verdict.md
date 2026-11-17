---
plan: 010-02_rsi-below-share-continuation_1d
idea: 010-02_rsi-below-share-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x coin excess 14-bar return on the non-overlapping grid: 0.0156167; t of the mean: 1.59469 (threshold: confirm if mean > 0 with t >= 2.0 (and support passes); reject if mean < 0 with t <= -2.0)
- Supporting check: Spearman(raw share below, excess 14-bar return) negative in at least 2 coins; per coin: BTCUSD=-0.008199432162361705, ETHUSD=-0.03894791824823208: 2, passed: True
- Counts: independent grid cases in total: 384, grid cases BTCUSD: 192, grid cases ETHUSD: 192, coins with negative Spearman: 2
- Decided by: t lies between -2.0 and 2.0, which the plan calls inconclusive.
- Reading: Grid bars are positions 0, 14, 28, ... of each window with t+14 inside the window; the coin's mean 14-bar return is the mean of its grid returns over all its windows; the supporting check keeps the plan's literal 'at least 2 coins negative' even though only the coins present in the record are tested.
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-02_rsi-below-share-continuation_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-02_rsi-below-share-continuation_1d`
Measure: `measure.py`
