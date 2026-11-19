---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins
line: 7.g patterns
backtest: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day move, in either direction, measured against its own 7-day hourly volatility, the larger its rise over the next day.
Consequence: After an unusually large daily move up or down, a trader has a reason to lean long the coin for the following day, and to refuse shorts that chase the move.
Why:
- F5: The next day's return, scaled by volatility, rises with the size of the past day's move whichever way it went: by quintile of the absolute 1-day z it goes 0.013 (t 0.93), 0.019, 0.019, 0.048 (t 2.40), 0.059 (t 3.60), with about 6056 daily cases per quintile; the largest falls (0.057, t 2.72) and the largest rises (0.050, t 3.23) are both followed by gains.
