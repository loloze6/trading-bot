---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is far further above its 200-day average than is usual for that coin, its rise over the next 20 bars is smaller than when it is moderately above.
Consequence: Scale down or refuse new longs when the price is extremely stretched above the long average, rather than adding size as the distance grows.
Why: F7: The most stretched closes give back their 20-day edge. The top quintile of raw distance above the SMA (mean 110%) has a next-20-bar return of only 0.0120, against 0.0596 for the fourth quintile (mean 41%), even though its next-day return is high at 0.0035.; F1: The trend effect is mostly in the large part of the forecast. On bars with a positive forecast, the gross position-weighted next-day return rises across forecast quintiles: −0.000089, 0.000772, 0.000511, 0.003418 and 0.005610. The next-20-bar return rises from −0.0012 in the lowest quintile (mean forecast 1.8) to +0.076 in the highest (mean forecast 20.0). The smallest forecasts, closes just above the 200-day SMA, earn nothing or lose.
