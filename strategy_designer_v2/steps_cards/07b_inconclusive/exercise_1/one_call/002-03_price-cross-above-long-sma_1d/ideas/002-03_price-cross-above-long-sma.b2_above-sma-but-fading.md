---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is above its 200-day SMA but lower than it was 20 bars ago, and the SMA itself is lower than 20 bars ago, the coin rises less than its average 20-bar move over the next 20 bars.
Consequence: Refuse or exit longs when the close is above the long average while price and the average are both falling over 20 bars.
Why:
- F4: Splitting by the past 20-bar return separates the bars. With a positive past 20-bar return, above-SMA bars earned +3.46% (hit 45.7%, trimmed +0.46%, non-overlapping t 1.25). With a negative one, they earned −2.75% (hit 37.5%, trimmed −4.33%, non-overlapping t −1.75).
- F5: Adding the SMA's own 20-bar slope sharpens the split.
- F1: On the 7,046 bars with forecast > 0, the next-20-bar excess return averaged +0.65% (naive t 1.83). The median was −3.06% and the hit rate 41.98%, with a standard deviation of 29.8% and skew 4.27. The top 5% of bars carry 656% of the summed excess, so a few large rallies drive the mean and noise swamps it.
