---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that closes near the low of its daily range rises over the next 1 day, and the closer the close sits to the day's low, the larger the next day's rise. Symmetrically, a close near the day's high is followed by a fall.
Consequence: A day's close location within its range gives a trader a graded one-day lean against where the day ended, usable on any day and not only after heavy-volume falls.
Why:
- F1: Where a coin closes inside its own daily range predicts the next day, and the effect is graded. Across all 17,379 bars, the next-day excess return falls as the close moves from the day's low to its high (slope -0.0031, t -4.67). The slope holds in both halves of the windows: w1-12 gives t -2.97 and w13-24 gives t -3.60. Closes in the bottom fifth of the range are followed by +0.35% (n 3,454, t 4.04), and closes in the top fifth by -0.22% (n 3,487, t -2.65).
