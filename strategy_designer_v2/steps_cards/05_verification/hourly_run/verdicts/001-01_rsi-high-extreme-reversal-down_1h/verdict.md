---
plan: 001-01_rsi-high-extreme-reversal-down_1h
idea: 001-01_rsi-high-extreme-reversal-down
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean fwd 12-bar log return after top-decile |forecast| minus drift: -0.00143263; t of the mean on non-overlapping 12-bar blocks: -1.23079 (threshold: confirm: pooled excess < 0 with t <= -2 and negative in >= 2 coins; reject: pooled excess > 0 with t >= +2; needs >= 30 non-overlapping extreme episodes per coin and >= 100 pooled)
- Supporting check: excess return falls across |forecast| quintiles (top minus neutral): 0.000454398, passed: False
- Counts: pooled non-overlapping extreme episodes: 390, coins with negative excess: 2, non-overlapping extreme episodes BTCUSD: 187, non-overlapping extreme episodes ETHUSD: 203
- Decided by: Pooled t lies between -2 and +2.
- Reading: Top decile is |forecast| >= its 90th percentile over all pooled bars (nonzero only), the drift is the mean forward 12-bar log return of all bars of the same coin and window, extreme episodes are extreme bars on the 0,12,24,... grid of each window, the supporting check uses all bars with zero-forecast bars as group 0 and needs a strictly falling mean plus a negative top-quintile excess in at least 2 coins, and with only the coins present the rule 'at least 2 of 3 coins' is applied as at least 2 coins.
Plan: `steps_cards/03_test_plan/hourly_run/plans/001-01_rsi-high-extreme-reversal-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/001-01_rsi-high-extreme-reversal-down_1h`
Measure: `measure.py`
