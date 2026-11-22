---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The higher a coin's volume over the past day relative to its 30-day average volume, the higher its return over the next three days.
Consequence: A day of unusually heavy trading is a reason to be long the coin for the next three days, and an unusually quiet day is a reason to refuse a long.
Why:
- F2: Recent volume grades the next three days. On non-overlapping 18-bar cells, the past day's volume against its 30-day average sorts the excess return from -0.55 % (t -2.27, 1032 cases, bottom quintile) to +0.80 % (t 2.56, 1032 cases, top quintile). Its Spearman with the excess return is +0.056 pooled and positive in all six coins (0.041 to 0.099, 858 cases each) and in 7 of 8 years (2022: -0.003). The top quintile's total move, about +1.2 %, is about six times the 0.19 % cost of a trade.
- F3: The direction of the past day's move changes what heavy volume means. In the top volume tercile, a 6-bar fall (lowest tercile of the vol-scaled 6-bar return) is followed by +1.07 % excess (691 cases), against -1.13 % for a flat day (310 cases). In the bottom volume tercile, a 6-bar rise is followed by -1.06 % (436 cases). Pooled, the lowest 6-bar-return quintile gives +0.84 % (t 3.07) and the Spearman is -0.052.
