---
plan: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h
idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean of forecast/10 x 168-bar excess return (non-overlapping, pooled): 0.0112801; t of the mean: 2.2767 (threshold: confirm: mean > 0 with t >= 2.0 and coin check passes; reject: mean < 0 with t <= -2.0; at least 300 cases)
- Supporting check: coins with mean product > 0 (need 2 of 3, of those present): 2, passed: True
- Counts: non-overlapping cases: 814, cases BTCUSD: 407, cases ETHUSD: 407
- Decided by: Pooled mean product is above 0 with t >= 2.0 and the coin check passes.
- Reading: The supporting check '2 of the 3 coins' is applied to the coins present in the record, requiring at least 2 coins with a positive mean product (all coins when only 2 are present); the coin's mean 168-bar return is the mean over its non-overlapping grid cases across all its windows; cases with forecast 0 are kept (product 0); the 300-case minimum, if unmet, gives 'not observable'.
Plan: `steps_cards/03_test_plan/retest_1h_run/plans/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h.md`
Record: `steps_cards/04_backtest/retest_1h_run/backtests/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h`
Measure: `measure.py`
