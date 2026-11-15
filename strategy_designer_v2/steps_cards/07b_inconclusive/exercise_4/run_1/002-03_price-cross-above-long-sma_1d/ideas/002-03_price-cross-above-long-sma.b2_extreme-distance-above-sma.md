---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day simple moving average, the further above it sits relative to its own past 200 days of distances, the larger the coin's gain over its average return over the next 20 days, with the gain concentrated in the most extreme distances.
Consequence: A trader would hold only when price is unusually far above its 200-day average for that coin, and treat a modest distance above it as no reason to be long.
Why:
- F3: Only the strongest forecasts show a gain, and even there the typical case loses. The top forecast quartile (mean forecast 19.3, n 100) has a mean 20-day excess of +0.072, but its median is -0.015 and only 42% of its cases beat holding. Quartiles 1 to 3 (forecasts 2.1 to 12.6) all have negative means (-0.035, -0.004, -0.013).
- F2: The positive mean comes from a few large gains, not from most cases. Above the SMA, the median 20-day excess is negative and the share beating holding is under 50% at every horizon: 46.9% at 5 days (n 1640), 44.9% at 10, 40.6% at 20, 37.7% at 40 (n 191) and 38.3% at 60 (n 120).
- F4: There is no grading by raw distance from the SMA. Across six sextiles running from -41% to +79%, the 20-day excess means are 0.001, 0.019, -0.016, -0.015, 0.012 and 0.013, and the two highest sextiles beat holding only 34.8% and 41.2% of the time.
