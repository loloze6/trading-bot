---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's one-day return on a Saturday or a Sunday, measured against its own recent daily volatility, is reversed over the next day. The larger the weekend day's rise, the larger the next day's fall, and the larger its fall, the larger the next day's rise.
Consequence: Fade each weekend day's move for one day in both directions, sized by how unusual the move was, and do not trade a weekday move the same way.
Why:
- F1: Weekend daily moves reverse the next day far more than weekday moves. Saturday and Sunday returns, scaled by the coin's own 20-day volatility, give a next-day excess-return slope of -0.0042 per unit. The Monday-to-Thursday slope is -0.0010 (n=19173), a difference with z = -4.67.
- F2: The weekend reversal holds widely and is graded in both directions. The slope is negative in 17 of 19 coins and in all 8 years (t from -0.59 in 2023 to -6.14 in 2019). By weekend-move quintile, the next-day excess return runs +0.53% (t 3.97, n=1919) after the largest falls, then -0.11%, -0.17%, -0.40%, and -0.56% (t -4.26, n=1919) after the largest rises.
- F5: Contrary to the brief, the weekend reversal is not stronger when volume is thin. By the bar's volume relative to its 28-day median, the slopes are -0.0039 (low tercile, t -2.54), -0.0043 (middle) and -0.0044 (high, t -5.42), about 3198 cases each.
