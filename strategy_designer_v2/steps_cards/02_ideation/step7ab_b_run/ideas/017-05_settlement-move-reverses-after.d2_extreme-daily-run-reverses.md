---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return relative to its usual 24-hour move, the larger its move in the opposite direction over the next 24 hours, with the reversal concentrated in the most extreme moves.
Consequence: A trader can lean against a coin's most extreme daily runs for a day, where the expected give-back is many times the cost of a trade.
Why:
- F1: The book loses because the move it bets on is far smaller than a trade's cost. Its 62,957 trades are held a median of 2 hours and average −0.10 % before fees and −0.20 % after, with 41 % winning. Over all its bars it earns 1.03 bps per unit traded, against about 10.5 bps of cost per unit (findings F1 and F4). The idea's own size is +0.05 % per case, 0.2 times the 0.21 % round trip.
- F5: The reversal reaches a size that pays only for the most extreme moves, and it keeps growing for a day. This was measured at all hours on a non-overlapping 8-hour grid:
- F6: The same tail reversal holds for longer moves, and it is largest over a day:
