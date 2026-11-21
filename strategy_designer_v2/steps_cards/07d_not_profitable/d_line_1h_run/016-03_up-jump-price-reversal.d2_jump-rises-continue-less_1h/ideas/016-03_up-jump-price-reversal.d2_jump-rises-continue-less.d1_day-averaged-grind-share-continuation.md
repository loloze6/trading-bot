---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of that rise that came from its few biggest hourly gains, the smaller the coin's further rise over the next 3 days, with that share read as its average over the past day rather than its value at the last hour.
Consequence: A trader would size long exposure on the day-long average of how grind-like the recent rise has been, so that hour-to-hour flicker in the share is no longer traded.
Why:
- F1: The book loses because fees eat more than the gross gain: across all coins it earns 3.05 bp a day before costs (1.97 bp from the coins' own rise and 1.08 bp from timing) but pays 8.18 bp a day in fees, about 10.8 bp per unit of turnover at 0.76 turnover a day, which leaves a mean daily return of -0.00052 and a Sharpe of -1.02.
- F2: The loss sits in short holds: the 6,981 trades under 2 hours average -0.72 % gross (-0.82 % net) and the 4,405 trades of 2–6 hours average -0.50 % gross, while the 3,098 trades of 24–72 hours average +5.04 % gross and the 573 trades over 72 hours average +14.55 % gross.
- F3: The forecast is jittery at the hourly scale: the raw residual switches between zero and positive 0.89 times a day, because the 72-hour return crosses zero and the three biggest hours enter and leave the 72-hour window. That switching produces most of the 0.76 daily turnover even though the effect plays out over 3 days.
- F4: The information survives in the slow part of the signal: on the non-overlapping 72-hour grid, the 24-hour average of the raw residual is still graded, with a next-72-hour return of 1.02 % in its top quintile, 0.38 % in the fourth and 0.09–0.10 % in the bottom three (about 1,108 cases each).
- F6: When the book is in, it gains 0.56 bp per hour gross against 1.01 bp per hour in fees. Holding the coin over the same hours would have earned 1.09 bp, so the position is right about direction but is churned too much to keep the gain.
