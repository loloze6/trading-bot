---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation
line: 7.g patterns
backtest: 016-05_up-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger the coin's absolute return over the past 3 days, in either direction, the more the coin rises over the next 3 days.
Consequence: Large 3-day swings, both rallies and sell-offs, are a reason to lean long for the following days rather than fade or chase their direction.
Why:
- F4: The size of the 3-day move matters in both directions, and the coin does better after large moves of either sign.
- F2: On up moves, the 3-day path efficiency predicts the next 3 days. Efficiency is the net 72-hour log move over the sum of absolute hourly moves. On the non-overlapping 72-bar grid, the top third minus the bottom third of excess forward return is +0.0092 − (−0.0032), Welch t 3.06, n 2865. All six coins are positive on the up side (t 0.88 to 2.18). Inside size terciles of the rise the sign holds but each tercile is weak alone (t 1.13, 0.73, 1.21). In a regression with size and volatility, the past × efficiency term is zero (t −0.01). Much of this effect is therefore the size of the rise.
