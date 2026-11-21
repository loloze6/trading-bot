---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the last 24 hours compared with its average daily volume over the past 30 days, the more it rises over the next 2 days.
Consequence: A trader leans long for two days after unusually heavy trading days, in proportion to how heavy they were.
Why:
- F4: The last 24 hours' volume over the coin's 30-day average daily volume predicts the next 48 hours. Its pooled slope t is +4.19 on the 48-hour excess (n 7859), positive on all 6 coins (+0.29 to +3.52) and in 6 of 8 years (2021 -2.19, 2022 -0.47). On net falls alone it is t +3.79. The top quintile ends +0.40 % above drift (t 1.96, strength 0.050), 2.1 times the cost.
- F3: Among net 24-hour falls, a hotter day leads to a larger rebound. The last 24 hours' volatility over the coin's 30-day volatility has a pooled slope t of +4.20 on the 48-hour excess (n 3841), positive on all 6 coins (t +1.33 to +2.00). Over all bars, the top quintile ends +0.52 % above drift (t 2.48, strength 0.064).
