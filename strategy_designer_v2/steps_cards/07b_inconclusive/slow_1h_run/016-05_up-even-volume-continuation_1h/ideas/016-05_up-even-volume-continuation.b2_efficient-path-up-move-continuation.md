---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation
line: 7.b inconclusive
backtest: 016-05_up-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of its hourly price movement over those 3 days that went into the net rise, the more the coin keeps rising over the next 3 days.
Consequence: An up move built from many small same-direction hourly steps is a reason to stay long for the next few days, and a choppy one of the same size is a reason not to.
Why:
- F5: Over all 3-day up moves, the price path's grind separates 72h outcomes where volume does not. The efficiency ratio (net 72h change over the sum of hourly absolute moves) gives a top-minus-bottom third excess 72h return of +0.0116 (Welch t 2.89, n 2865). Its top third is +0.0081 and its bottom third -0.0036.
- F8: Volume evenness and price-path grind are largely different measures. The tested forecast has a rank correlation of only -0.135 with the top-3-hour concentration. So the test measured the brief's "grind" through volume, while the effect shows through the shape of the price path.
