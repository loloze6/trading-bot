---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return, the price rises over the next 1 day by more than the coin's usual 1-day move. The larger the drop in those multiples, the larger the rise.
Consequence: A trader should refuse to short a fresh hourly plunge and instead treat it as a reason to buy for a day, because the move that follows is a rebound several times the cost of a trade.
Why:
- F1: The book loses by being short almost all the time against coins that rise. It was short on 95.8 % of bars with a mean allocation of -0.78, and it lost 0.42 bps per bar: -0.47 bps came from the coins' own rise and only +0.05 bps from timing. It closed 8287 short trades with a mean of -5.7 % before fees. Its forecast is non-zero on any negative 24-hour return, so 202702 bars were active.
- F3: Over the 5-day horizon there is no continuation after a large 24-hour drop.
- F4: Over the next day a large 24-hour drop is followed by a rebound, and the rebound grows with the drop.
