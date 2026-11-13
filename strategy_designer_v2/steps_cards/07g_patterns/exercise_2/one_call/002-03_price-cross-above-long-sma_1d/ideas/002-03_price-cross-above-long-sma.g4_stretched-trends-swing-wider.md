---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits far above its 200-day SMA, its daily returns swing about twice as wide in both directions as when it sits near or below the average.
Consequence: A trader could cut size when the close is far above the long average instead of adding on distance, as the forecast does.
Why:
- F5: The book's best and worst 1% of days (171 each, mean +27.7% and −22.5%) both come when the close sits far above its 200-day SMA (median distance 114% and 59%, against −1.5% on other days), with the forecast near its cap (19.7 and 15.1) and the trailing 20-day volatility near 0.079–0.080, against 0.042 on other days.
- F6: The distance above the 200-day SMA does not sort forward returns: across the ten distance deciles the 20-bar excess t-statistics all lie between −0.34 and 0.86, and on bars above the SMA only 42% of 20-bar returns beat the coin's mean.
