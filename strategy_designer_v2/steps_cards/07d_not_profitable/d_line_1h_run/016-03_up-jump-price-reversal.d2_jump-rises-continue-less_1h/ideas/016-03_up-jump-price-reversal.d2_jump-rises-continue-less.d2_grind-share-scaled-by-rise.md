---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of that rise that came from its few biggest hourly gains, the smaller the coin's further rise over the next 3 days, and this gap widens the larger the 3-day rise itself.
Consequence: A trader would put most of the long exposure into large grind-built rises and hold little after small rises, where the share carries almost no information and only costs fees.
Why:
- F1: The book loses because fees eat more than the gross gain: across all coins it earns 3.05 bp a day before costs (1.97 bp from the coins' own rise and 1.08 bp from timing) but pays 8.18 bp a day in fees, about 10.8 bp per unit of turnover at 0.76 turnover a day, which leaves a mean daily return of -0.00052 and a Sharpe of -1.02.
- F5: The grind effect is strongest where the 3-day rise is large. Among big rises, grind-built ones return 1.51 % over the next 72 hours against 0.81 % for jump-built ones (477 vs 478 cases). Among mid rises the figures are 1.11 % against 0.10 % (254 vs 701 cases). Among small rises it is almost never present (12 cases).
- F6: When the book is in, it gains 0.56 bp per hour gross against 1.01 bp per hour in fees. Holding the coin over the same hours would have earned 1.09 bp, so the position is right about direction but is churned too much to keep the gain.
