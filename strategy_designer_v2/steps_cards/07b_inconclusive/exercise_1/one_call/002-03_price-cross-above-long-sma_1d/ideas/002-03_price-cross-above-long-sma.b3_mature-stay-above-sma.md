---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close has stayed above its 200-day SMA for more than 60 consecutive bars, the coin rises more than its average 20-bar move over the next 20 bars.
Consequence: Trust established stays above the long average rather than fresh crosses, which tend to lag the coin.
Why:
- F7: The effect also depends on how long the close has been above the SMA.
- F6: The effect sits in the largest forecasts. By forecast quintile, the excess rose from −2.72% and −2.26% in the two lowest to +5.15% in the top one. Forecast ≥ 10 combined with a rising past 20-bar return gave +5.29% on 2,250 bars (hit 45.9%, t 1.39).
- F1: On the 7,046 bars with forecast > 0, the next-20-bar excess return averaged +0.65% (naive t 1.83). The median was −3.06% and the hit rate 41.98%, with a standard deviation of 29.8% and skew 4.27. The top 5% of bars carry 656% of the summed excess, so a few large rallies drive the mean and noise swamps it.
