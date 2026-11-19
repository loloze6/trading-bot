---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the higher its daily volume relative to its own 20-day average volume, the higher its return over the next 3 days, only while its 7-day volatility of hourly returns is high against its 30-day volatility, and the more so the higher that ratio.
Consequence: A trader should take heavy-volume longs in a rising coin mainly when its volatility is expanding, and refuse them when its recent volatility is compressed, because those trades pay mostly fees.
Why:
- F2: Nearly all the net gain comes from bars where volatility has expanded. In the top quartile of 7-day over 30-day hourly volatility (1.14 to 1.97), the position nets 6.38 of the total 6.80, with the coin rising 2.43 bp per hour. In the bottom quartile (0.30 to 0.81), it nets 0.02, with the coin rising 0.36 bp per hour.
- F3: On the book's days, the lowest quartile of that volatility ratio (mean 0.70) loses 0.000119 per day net, and 44 % of those days sit more than 10 % below the book's peak. The highest quartile (mean 1.26) earns 0.001059 per day, and 34 % of its days are in such a fall.
- F4: The book's deepest fall is -24.1 %, and windows w8 to w17 hold falls of -18 % to -24 %. The 1105 days spent more than 10 % below the peak average a gross return of -0.000181 per day and fees of 0.000222. The other 1817 days average a gross return of +0.001166.
