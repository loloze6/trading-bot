---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 001-03_rsi-high-extreme-continuation_config.json
Confirm: The horizon is 5 bars (5 days). Take the bars whose forecast is in that coin's top decile, which are the highest RSI readings. On at least 2 of the 3 coins, and with no coin showing the opposite, the mean 5-bar forward return after those bars must exceed both of these by more than one standard error: the mean 5-bar forward return after neutral bars (forecast above 0 but below the median of the positive forecasts), and the coin's unconditional mean 5-bar return. The strategy's return before costs must also beat buy-and-hold scaled to the strategy's average exposure.
Reject: On at least 2 of the 3 coins, the mean 5-bar forward return after top-decile forecast bars is at or below the neutral-bar mean and the unconditional mean. A clear reversal, where the top-decile return falls below the neutral-bar return by more than one standard error, rejects the idea and points to the reversal reading.
Inconclusive: The coins split in sign, or the top-decile minus neutral difference stays within one standard error on two or more coins.
Deviation: "After RSI reaches a high extreme" is tested as a position held while RSI is above 50, growing with the square of RSI's distance above 50, so extremes dominate. There is no fixed threshold such as 70 and no explicit post-event window. The position is flat whenever RSI is below 50, so low extremes are not tested.
