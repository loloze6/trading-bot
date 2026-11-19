---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly returns over the past 1 day have been calm, the larger its 1-day move, the more it keeps moving the same way over the next 3 days.
Consequence: Follow a calm day's move for several days instead of fading it.
Why:
- F4: The level of recent volatility decides the sign of the effect: in the top tercile of 24h hourly volatility the 24h slope on the past 24h move is -0.0058 (t -10.1, n 5607), while in the bottom tercile it is +0.0027 (t 2.17) at 24h and +0.0127 (t 3.13, n 1846) at 72h; by volatility quintile, the next-day move in the past move's direction is -0.60% (t -4.55) in the top quintile against +0.03% (t 0.50) in the bottom.
