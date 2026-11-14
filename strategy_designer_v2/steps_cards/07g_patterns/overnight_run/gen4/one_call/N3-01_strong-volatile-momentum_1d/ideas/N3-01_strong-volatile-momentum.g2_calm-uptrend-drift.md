---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-01_strong-volatile-momentum
line: 7.g patterns
backtest: N3-01_strong-volatile-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin is up over both 20 and 60 days while its 20-day volatility is in the lower half of its recent range, its next 5 days rise more than its average. Calm uptrends carry the drift better than volatile ones.
Consequence: A trader can take trend longs in calm uptrends rather than only in volatile ones.
Why:
- F4: Bars with both the 20-day and the 60-day return positive are followed by a 5-bar excess of +0.0103 (t=2.35, n=600 non-overlapping). Most of this comes from bars the strategy left flat because volatility was below its threshold or the forecast was zero: +0.0163 (t=2.40, n=281). The bars it traded show only +0.0050 (t=0.88, n=319). The high-volatility filter therefore removes the better part of the trend drift.
