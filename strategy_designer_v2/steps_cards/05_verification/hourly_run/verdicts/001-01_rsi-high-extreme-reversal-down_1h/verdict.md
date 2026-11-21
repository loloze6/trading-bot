---
plan: 001-01_rsi-high-extreme-reversal-down_1h
idea: 001-01_rsi-high-extreme-reversal-down
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 12-bar log return after top-decile |forecast| bars minus coin's unconditional mean: -0.00130566; t of the mean on non-overlapping 12-bar blocks: -1.11908 (threshold: confirm: negative with t <= -2 and negative in >= 2 coins; reject: positive with t >= +2)
- Supporting check: excess return falls steadily from neutral (zero) group through |forecast| quintiles 1-5, and top-minus-neutral negative in >= 2 coins (value: Q5 minus neutral): -0.00114271, passed: False
- Counts: pooled extreme episodes: 390, extreme episodes BTCUSD: 187, extreme episodes ETHUSD: 203, coins with negative excess: 2
- Decided by: Pooled t lies between -2 and +2.
- Reading: Top decile is the 90th percentile of |forecast| over all bars pooled across coins and windows (nonzero only), returns are 12-bar log returns on each window's 0,12,24,... grid with each coin's drift being its mean over all its windows, quintiles are pooled quintiles of nonzero |forecast| with zero-forecast bars as neutral, 'steadily' means each group mean is no higher than the previous one, and with only BTC and ETH present the '2 of 3 coins' rules need both coins and the per-coin minimums apply to the coins present.
- Size: unusual move +0.06 % per case over 12 bars, 0.027 of the coin's usual move (2.30 %); normal drift in its direction -0.01 %, total +0.05 %; 1765 cases
Plan: `steps_cards/03_test_plan/hourly_run/plans/001-01_rsi-high-extreme-reversal-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/001-01_rsi-high-extreme-reversal-down_1h`
Measure: `measure.py`
