---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 1 day runs against its own 1-day return, and the larger the past day's move relative to the coin's recent volatility, the larger the move back.
Consequence: After an outsized daily move, lean the other way for the next day rather than follow it.
Why:
- F3: Over the day after a 24-hour move, returns run against that move. Pooled over non-overlapping 24-hour cases, the slope is -24.0 bp per z (t -5.5, n 12,926) and it is negative in all six coins (t from -1.8 to -3.3). By quintile of the past 24-hour return, the bottom quintile is followed by +43.9 bp (t 4.3) and the top by -30.0 bp (t -3.1).
