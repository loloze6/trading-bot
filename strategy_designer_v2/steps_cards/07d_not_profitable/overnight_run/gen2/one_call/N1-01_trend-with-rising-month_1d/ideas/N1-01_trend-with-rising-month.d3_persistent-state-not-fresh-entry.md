---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-01_trend-with-rising-month
line: 7.d not profitable
backtest: N1-01_trend-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose close has stayed above its 200-day average with a positive 20-bar return on most of the last 20 bars keeps rising over the next 20 bars, while a coin that has only just entered that state tends to fall back out of it.
Consequence: Enter the trend long only once the up state has held for a while, rather than on its first day, to avoid the many short losing spells.
Why:
- F3: The book is a lottery on a few long trends.
- F2: The forecast has no measurable edge at the 20-bar horizon. On active bars, the forward 20-bar excess return is +1.5% with t=0.63 over 251 non-overlapping cases, and the forecast>2.5 bucket gives +1.45% with t=0.59 over 242 cases. A larger forecast does not earn more: the four entry-forecast quartiles average a gross gain of 6.2%, 4.3%, 2.3% and 7.8% per trade.
