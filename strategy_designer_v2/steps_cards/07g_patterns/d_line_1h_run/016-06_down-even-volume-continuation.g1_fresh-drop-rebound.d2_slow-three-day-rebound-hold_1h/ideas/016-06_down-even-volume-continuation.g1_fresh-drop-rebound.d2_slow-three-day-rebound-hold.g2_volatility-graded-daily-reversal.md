---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more volatile a coin's hourly returns have been over the past 1 day, the more its 1-day move reverses over the next 1 day.
Consequence: Lean against a coin's last-day move in proportion to how turbulent its hours have just been.
Why:
- F4: The level of recent volatility decides the sign of the effect: in the top tercile of 24h hourly volatility the 24h slope on the past 24h move is -0.0058 (t -10.1, n 5607), while in the bottom tercile it is +0.0027 (t 2.17) at 24h and +0.0127 (t 3.13, n 1846) at 72h; by volatility quintile, the next-day move in the past move's direction is -0.60% (t -4.55) in the top quintile against +0.03% (t 0.50) in the bottom.
- F3: Measured unconditionally on a 24h grid, the lowest quintile of 24h move is followed by +0.48% excess over the next 24h (t 4.59, n 3308), and the highest quintile by -0.32% (t -3.24, n 3305).
