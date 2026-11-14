---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 001-03_rsi-high-extreme-continuation_config.json
Confirm: On each coin, the bars with the largest long positions (RSI far above 50, top decile of the forecast) are followed by next-1 to next-10-day returns that are clearly higher than the returns after bars with zero or small positions. The portfolio's gain per unit of position should also rise with position size, and the strategy should beat simply holding the coin before costs, on all three coins.
Reject: Returns after the largest positions are no higher than after zero or small positions, or are lower (reversal), so gains do not grow with position size. The strategy is also no better than holding the coin before costs, or the result holds for only one of the three coins.
Deviation: The config trades only the high side. Positions are long, growing with how far RSI(14) is above 50, and squared so the extremes get most of the weight. Flat when RSI is below 50. "Extreme" becomes a graded size rather than a threshold event, and the "neutral" comparison is the near-zero positions. Holding is continuous while RSI stays high, not just once after the extreme is reached.
