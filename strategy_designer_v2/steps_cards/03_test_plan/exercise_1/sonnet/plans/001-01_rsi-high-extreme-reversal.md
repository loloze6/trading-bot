---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 001-01_rsi-high-extreme-reversal_config.json
Confirm: On each coin, the daily returns after the most negative forecasts (the largest shorts, highest RSI) are clearly below the coin's average daily return over the whole period, and the short position's gross gain per bar rises as the position gets larger. It should also beat holding the coin, measured before costs.
Reject: Returns after the largest shorts are equal to or above the coin's unconditional average, or the short's gross gain is flat or falls as position size grows. Then the high-RSI reading shows no reversal (continuation or nothing), and the short-only portfolio does no better than holding.
Deviation: "Price falls over the following bars after an extreme" becomes "hold a short while RSI(14) is above 50, sized by how high it is against its own recent history and amplified toward extremes by squaring, fading as RSI falls back". It does not wait for a discrete extreme event or hold for a fixed number of bars, and it takes no long position when RSI is low, since the idea concerns only the high extreme.
