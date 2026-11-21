---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 2-hour move relative to its usual 2-hour move, the more of it the coin gives back over the next 24 hours, with the give-back growing fastest for the most extreme moves.
Consequence: Fading a coin's most violent 2-hour moves and holding for a day captures a reversal several times a round trip, while fading ordinary moves does not cover costs.
Why:
- F1: The book loses because the move it bets on is far smaller than a trade's cost. Its 62,957 trades are held a median of 2 hours and average −0.10 % before fees and −0.20 % after, with 41 % winning. Over all its bars it earns 1.03 bps per unit traded, against about 10.5 bps of cost per unit (findings F1 and F4). The idea's own size is +0.05 % per case, 0.2 times the 0.21 % round trip.
- F3: The effect is not tied to funding settlement. At non-settlement clock hours (bar starts 03, 11 and 19 UTC), the same signed 2-hour reversal is larger, 4.8 bps on average with t 8.23, against t 5.57 at settlement. In the top tenth of moves it is 23.0 bps against 10.0 bps. This meets the brief's own third falsification condition: the effect appears just as strongly when no funding is settled.
- F5: The reversal reaches a size that pays only for the most extreme moves, and it keeps growing for a day. This was measured at all hours on a non-overlapping 8-hour grid:
- F7: The book's sizing also cuts it off where the move would pay. The forecast is capped at ±20, and its top fifth by forecast size (entries near 19.9) is the worst: −0.20 % before fees per trade, against about −0.08 % for the other fifths. The capped trades do not get a 24-hour hold, which is the horizon over which the large reversals of F5 build.
