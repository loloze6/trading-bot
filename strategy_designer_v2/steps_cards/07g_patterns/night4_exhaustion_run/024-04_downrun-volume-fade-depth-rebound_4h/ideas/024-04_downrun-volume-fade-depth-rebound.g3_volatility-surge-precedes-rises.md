---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The more a coin's volatility over the past 5 days exceeds its volatility over the past 30 days, the higher its return over the next three days.
Consequence: A turbulence surge is a reason to hold the coin long for three days, and a stretch of unusual calm is a reason to refuse a long.
Why:
- F4: Calm periods underperform and turbulent ones outperform. The ratio of 5-day to 30-day volatility sorts the 18-bar excess return from -0.64 % (t -2.66, lowest quintile) to +0.71 % (t 2.32, highest quintile), with a Spearman of +0.040.
- F2: Recent volume grades the next three days. On non-overlapping 18-bar cells, the past day's volume against its 30-day average sorts the excess return from -0.55 % (t -2.27, 1032 cases, bottom quintile) to +0.80 % (t 2.56, 1032 cases, top quintile). Its Spearman with the excess return is +0.056 pooled and positive in all six coins (0.041 to 0.099, 858 cases each) and in 7 of 8 years (2022: -0.003). The top quintile's total move, about +1.2 %, is about six times the 0.19 % cost of a trade.
