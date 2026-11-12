---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is above its 200-day SMA, that SMA is higher than 20 bars ago, and the close is also higher than 20 bars ago, the coin rises more than its average 20-bar move over the next 20 bars.
Consequence: Take long trend trades above the long average only when both price and the average are rising over the last 20 bars, and refuse the rest.
Why:
- F4: Splitting by the past 20-bar return separates the bars. With a positive past 20-bar return, above-SMA bars earned +3.46% (hit 45.7%, trimmed +0.46%, non-overlapping t 1.25). With a negative one, they earned −2.75% (hit 37.5%, trimmed −4.33%, non-overlapping t −1.75).
- F5: Adding the SMA's own 20-bar slope sharpens the split.
- F8: With past 20-bar momentum up, the result holds across most coins. BTC had median +0.29% and hit 51.0%; ETH +0.81% and hit 52.2%; ZEC +0.25% and hit 50.6%. XMR was the exception at −0.23% mean and 42.7% hit.
