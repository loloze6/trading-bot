---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past week is high, the deeper its fall over the past day relative to that volatility, the more it rises over the next day.
Consequence: A trader would buy sharp one-day falls in volatile conditions, sized by how deep the fall was against recent volatility, and would refuse to short them.
Why:
- F1: Over one day, sharp falls bounce back. On the non-overlapping 24-hour grid, the most negative fifth of 24-hour returns (scaled by the past week's hourly volatility) was followed by a next-day excess return of +0.0043 (t 4.33, 3251 cases). The other four fifths all had excess returns between -0.0007 and -0.0019. Fitted on falls alone, the slope of next-day excess return on the scaled 24-hour move is -0.0047 (t -5.00, 7974 cases); on rises alone it is -0.0006 (t -0.75, 8241 cases).
- F2: That one-day reversal sits almost entirely in the most volatile third of each coin's days. There the slope is -0.0076 (t -8.17, 5413 cases). In the middle third it is +0.0006 (t 1.02) and in the calmest third +0.0011 (t 2.25). The slope is negative for all six coins (t -1.5 to -3.4) and in 6 of 8 years.
