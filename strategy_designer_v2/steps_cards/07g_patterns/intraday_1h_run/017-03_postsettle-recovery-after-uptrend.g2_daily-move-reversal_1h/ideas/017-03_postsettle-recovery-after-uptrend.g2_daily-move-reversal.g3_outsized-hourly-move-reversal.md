---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 1 hour runs against its past 1-hour return, and the larger that move in units of the coin's 7-day hourly volatility, the larger the move back.
Consequence: After an outsized hourly move, expect a partial give-back within the hour, larger for larger moves; fees matter at this horizon.
Why:
- F5: Hourly bars reverse, and the reversal grows with the size of the last hour's move in units of its 7-day hourly standard deviation. Across quintiles of |1h move| the reversal product rises from 0.0000006 (t 0.18) to 0.00098 (t 6.66), with about 78,490 cases each. It is positive in 41 of 48 coin-years.
