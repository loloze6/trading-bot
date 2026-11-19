---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past 3 days, the more it rises over the next 3 days.
Consequence: A trader would lean long after deep 3-day falls, sized by the fall's depth, rather than follow them down.
Why:
- F3: Over 3 days, rises and falls behave in opposite ways. After a 3-day fall, the next 3-day excess return has a slope of -0.104 on the size of the fall (t -3.56, 2669 cases), so deeper falls rebound more. After a 3-day rise the slope is +0.067 (t 2.81, 2865 cases).
- F1: Over one day, sharp falls bounce back. On the non-overlapping 24-hour grid, the most negative fifth of 24-hour returns (scaled by the past week's hourly volatility) was followed by a next-day excess return of +0.0043 (t 4.33, 3251 cases). The other four fifths all had excess returns between -0.0007 and -0.0019. Fitted on falls alone, the slope of next-day excess return on the scaled 24-hour move is -0.0047 (t -5.00, 7974 cases); on rises alone it is -0.0006 (t -0.75, 8241 cases).
