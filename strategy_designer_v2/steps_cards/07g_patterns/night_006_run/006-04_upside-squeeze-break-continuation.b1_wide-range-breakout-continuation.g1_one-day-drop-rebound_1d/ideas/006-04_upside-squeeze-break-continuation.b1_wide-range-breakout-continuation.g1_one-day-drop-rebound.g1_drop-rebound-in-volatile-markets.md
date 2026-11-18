---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 60-day volatility, the larger the rebound over the next 1 day per unit of its 1-day fall (measured in its usual daily moves).
Consequence: A trader would lean long after sharp one-day drops mainly when the coin has been volatile, scaling with that volatility, and stand aside when the coin has been calm.
Why:
- F1: The rebound after a fall depends on how volatile the coin already is. In the coin's highest third of 60-day volatility, the slope of next-day excess return on the size of the fall is 0.0147 (t 7.09, n 2360). In the middle third it is 0.0042 (t 3.27, n 2454). In the lowest third it is -0.0001 (t -0.11, n 2337).
- F2: Only falls rebound; rises do not, and only the largest falls carry the effect.
- F7: The book's tails are about 0.7 times those of holding the coins. Its worst 1% of days average -0.080 against -0.112 for the coins on the same days, and its best 1% average +0.070 against +0.106. This means the falls it buys keep falling on crash days, which is consistent with the failed Calmar of 0.70.
