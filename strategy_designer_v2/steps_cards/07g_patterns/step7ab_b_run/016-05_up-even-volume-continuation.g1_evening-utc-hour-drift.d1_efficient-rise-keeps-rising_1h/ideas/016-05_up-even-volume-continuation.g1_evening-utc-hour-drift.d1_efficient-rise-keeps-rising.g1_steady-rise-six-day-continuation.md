---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising
line: 7.g patterns
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more efficiently a coin has risen over its past 3 days (its 3-day rise large relative to the sum of its absolute hourly moves, judged against that coin's whole history rather than its recent month), the more it keeps rising over the next 6 days.
Consequence: An unusually steady 3-day rise is a reason to stay long for about a week, with an excess move several times a round trip, while ordinary rises are not.
Why:
- F1: Among 3-day rises, the coin's excess return over the next 3 days is carried almost entirely by the most efficient fifth. Those cases have a raw efficiency ratio averaging 0.27 and earn +1.13 % above the coin's normal drift (t 2.78, 574 cases), about 6 times the backtest's 0.19 % round trip; the other four fifths range from -0.44 % to +0.33 %, none with |t| above 1.3.
- F2: The same top fifth of efficient 3-day rises keeps outperforming at twice the horizon: over the next 6 days its excess return is +0.167 of the coin's usual move (t 3.42, 562 cases), while the other fifths range from -0.050 to +0.016, all with |t| below 1.2.
- F3: The tested forecast blurs this effect. It standardises efficiency against its recent month and correlates only 0.72 with the raw ratio. Its top fifth earns +0.68 % in excess over 3 days (t 1.76), against +1.13 % (t 2.78) for the raw ratio's top fifth on the same cases.
- F5: The continuation of efficient rises is not stable across the record. The top-efficiency fifth earns +0.259 of a usual move in windows 13 to 24 (t 3.45, 295 cases) but only +0.017 in windows 1 to 12 (t 0.33, 280 cases). Five of six coins show a positive efficiency slope after controlling for size (t 1.0 to 1.7); ZEC is negative (t -0.41).
