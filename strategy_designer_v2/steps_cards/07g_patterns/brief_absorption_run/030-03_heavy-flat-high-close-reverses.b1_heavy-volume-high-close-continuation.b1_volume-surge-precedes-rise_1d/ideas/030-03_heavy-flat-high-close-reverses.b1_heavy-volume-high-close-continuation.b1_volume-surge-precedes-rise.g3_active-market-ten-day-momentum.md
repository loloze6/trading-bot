---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is middling to high, the larger its 10-day return, the more it keeps rising over the next 10 days, and the larger its 10-day fall, the more it keeps falling.
Consequence: Once a coin is moving actively, a trader follows its 10-day move for the next 10 days, more so the larger the move, and refuses to fade it.
Why:
- F3: The momentum effect is absent in calm conditions. In the lowest 20-day-volatility tercile the 10-day-return slope is 0.044 (t 1.14, n 468), against 0.124 (t 2.88, n 467) in the middle tercile and 0.103 (t 1.99, n 468) in the high tercile. It is positive for 5 of 6 coins (ZEC t 2.70, LTC -0.45), but it changes sign by year (2020 t 3.21, 2018 t -1.34).
- F1: The coin's own 10-day return scaled by its 20-day daily volatility predicts its excess return over the next 10 days. On the non-overlapping 10-day grid, the pooled slope of the standardised excess return on it is 0.092 with t 3.58 over 1403 independent cases. That is stronger than the tested volume-ratio slope measured the same way, 0.045 with t 1.75 over 1403 cases.
