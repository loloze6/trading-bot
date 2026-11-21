---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising
line: 7.g patterns
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For 3-day rises of the same efficiency, the smaller the rise relative to the coin's usual 3-day move, the more the coin keeps rising over the next 3 days.
Consequence: A steady but modest 3-day rise is a better reason to be long than a large one of equal steadiness, which is more likely already spent.
Why:
- F4: Across all 3-day moves, the next 3 days' return in the move's direction, in units of the coin's usual move, rises with efficiency and falls with size and jumpiness. A regression on about 5,540 grid cases gives coefficients of +0.71 on efficiency (t 3.17), -0.067 on the move's size in standard deviations (t -2.36) and -0.86 on the largest hour's share of absolute moves (t -1.91). For a given size, steadier moves continue more, and larger or jump-made moves continue less.
- F1: Among 3-day rises, the coin's excess return over the next 3 days is carried almost entirely by the most efficient fifth. Those cases have a raw efficiency ratio averaging 0.27 and earn +1.13 % above the coin's normal drift (t 2.78, 574 cases), about 6 times the backtest's 0.19 % round trip; the other four fifths range from -0.44 % to +0.33 %, none with |t| above 1.3.
