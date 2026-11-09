---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 001-01_rsi-high-extreme-reversal_config.json
Confirm: At a 5-bar horizon, on each of BTC, ETH and BNB, the mean forward 5-bar return after the largest short positions (top decile of |forecast|) is negative and below that coin's mean 5-bar return over all bars. The short-only portfolio, before costs, also gains on those bars, with gains growing from the smaller to the larger positions.
Reject: On at least two of the three coins, the mean 5-bar forward return after the largest short positions is at or above the coin's all-bar mean, which is no reversal or continuation. Alternatively, the short positions lose money before costs, with losses growing with position size.
Inconclusive: Results that differ by coin (one confirms, another rejects, the third is flat). Fewer than about 20 largest-position bars on a coin. A negative forward return that is not below the coin's all-bar mean (market drift only). A sign that appears at other horizons but not at 5 bars.
Deviation: The config tests only the high side (RSI above 50, short), with no long on low RSI. "After the index reaches an extreme" becomes "while RSI is elevated, short in proportion to the squared standardised distance above 50". The position is held while the reading stays high, not triggered once on an event, and the size is relative to each coin's own recent RSI deviations rather than a fixed RSI level such as 70.
