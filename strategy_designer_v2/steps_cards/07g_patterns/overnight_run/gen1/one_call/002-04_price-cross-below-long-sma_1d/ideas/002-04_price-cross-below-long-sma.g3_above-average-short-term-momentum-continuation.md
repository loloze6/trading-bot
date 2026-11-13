---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is above its 200-day average and its 5-day return is among its strongest, the coin keeps rising over the next ten days.
Consequence: Trend-following entries work better as longs on strong short-term gains above the long average than as shorts below it.
Why:
- F5: While above the SMA200, the top quintile of 5-day returns is followed by a 10-bar return of +3.88% (t 7.6, overlapping) and +3.60% in non-overlapping blocks (t 2.3, n 197). The lower three quintiles give +0.1% to +0.4%. Below the SMA200, the 5-day return gives no such ordering. The effect was negative in 2018 to 2019 (n 8 and 18).
