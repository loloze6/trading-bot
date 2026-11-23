---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The nearer a coin closes to its day's low on a down day whose volume is heavy against its prior 20-day average, the more it rises over the next day. The higher its 20-day volatility against its own past level, the larger that rise.
Consequence: A trader buys after heavy-volume falls that close at the low mainly when the coin is turbulent, and refuses them when it is calm.
Why:
- F5: The tested idea's top fifth of down-day forecasts earns only when volatility is high. Next-day excess return is +1.50 % (t 6.01, 754 days) in the high-volatility third, +0.21 % (t 1.40) in the middle third and -0.13 % (t -1.04) in the low third.
- F6: Close location and volume still carry their own information on down days. With the volatility-scaled return in the regression, the closeness to the low × log volume ratio has t 4.38 and the volatility-scaled return itself has t 0.03 (7151 days).
- F1: The coin's 20-day volatility sets the size of the next-day reversal. In the coins' own top third of 20-day volatility, a down day is followed by a next-day excess return of +0.71 % (t 5.59, 2357 days) and an up day by -0.36 % (t -3.20, 2491 days). In the bottom third, down days are followed by -0.16 % (t -2.03) and up days by -0.00 % (t -0.03).
