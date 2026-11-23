---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin rises over the two hours ending 23:00 UTC. The rise is larger the higher the coin's current 30-day usual move stands against its own usual level of the past three months, and the further the coin fell over the previous 24 hours.
Consequence: A trader would favour longs held through the late-evening UTC hours after a falling day in a volatile market, and refuse shorts held over them.
Why:
- F6: The two hours closing at 23:00 UTC (the 21:00 and 22:00 UTC hourly bars) rise on average by +0.097 % (t 9.1, 17403 cases). The rise is positive in 7 of 8 years (2022 is -0.04 %), in every coin (t 3.1 to 4.7) and on every weekday (t 2.1 to 4.4). It is larger in high volatility (+0.144 %, t 6.2) than in low volatility (+0.071 %, t 3.6). It is also larger after a 24h fall (+0.144 % in the lowest third of prior z, against +0.079 % in the highest; slope on z t -3.3). Even in high volatility the move is below the 0.19 % cost of a trade.
