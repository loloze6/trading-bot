---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits only slightly above its 200-day average compared with its usual distance, the price falls back below the average within days more often than it keeps rising.
Consequence: Refuse fresh, marginal crosses above the long average and enter only once the close stands clearly above it, to cut the short losing trades.
Why: F1: The trend effect is mostly in the large part of the forecast. On bars with a positive forecast, the gross position-weighted next-day return rises across forecast quintiles: −0.000089, 0.000772, 0.000511, 0.003418 and 0.005610. The next-20-bar return rises from −0.0012 in the lowest quintile (mean forecast 1.8) to +0.076 in the highest (mean forecast 20.0). The smallest forecasts, closes just above the 200-day SMA, earn nothing or lose.; F3: Fees are not the problem; whipsaw is. The 2228 trades, all long, average a 4.23% gain before fees and 4.13% after. Only 29.7% win. The three shorter duration quartiles (about 1.8, 6.5 and 18.1 days held) lose −6.26%, −5.75% and −2.47% before fees. Only the longest quartile (about 58.7 days) earns, at +31.41%.
