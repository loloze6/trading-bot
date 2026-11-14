---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin has stayed below its 200-day average for a long stretch of months, it keeps falling over the next 20 bars more often than it rises.
Consequence: A trader should refuse bottom-fishing longs in a coin that has spent a long time below its long average.
Why:
- F5: Time spent in a state matters on both sides. Bars that had been below the SMA for 60–150 days returned −1.29% over 20 bars with a 32.5% hit rate (n=1,492). Bars below for 5–60 days returned +3.95% to +4.36% with hits of 47–48%. Bars above for 60–150 days had a +6.01% mean but only a 34.3% hit rate.
