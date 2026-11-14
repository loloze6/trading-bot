---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin has recently dropped below its 200-day average, within the past several weeks, it rises over the next 20 bars more than its usual drift. The rise starts with a short bounce in the first days after the cross down.
Consequence: A trader can treat a fresh drop below the long average as a short-term buying opportunity rather than an exit signal.
Why:
- F5: Time spent in a state matters on both sides. Bars that had been below the SMA for 60–150 days returned −1.29% over 20 bars with a 32.5% hit rate (n=1,492). Bars below for 5–60 days returned +3.95% to +4.36% with hits of 47–48%. Bars above for 60–150 days had a +6.01% mean but only a 34.3% hit rate.
- F6: The cross events themselves show little continuation. After an upward cross (n=278), the next 5 bars returned +0.05% and the next 20 returned +2.47% (median +1.57%, hit 44.6%). After a downward cross (n=280), the next 5 bars returned +0.92%, a short-term bounce, while the next 20 had a +1.09% mean but a −1.30% median and a 39.6% hit rate.
