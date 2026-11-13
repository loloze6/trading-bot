---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-01_trend-with-rising-month
line: 7.d not profitable
backtest: N1-01_trend-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that closes above its 200-day average with a positive 20-bar return keeps rising faster than its own average over the next 20 bars mainly when its 60-bar return is also positive, that is, when the short rise belongs to an older, established up-trend.
Consequence: Take the trend long only when the 60-bar return is also up, and refuse fresh bounces inside a falling quarter.
Why:
- F2: The forecast has no measurable edge at the 20-bar horizon. On active bars, the forward 20-bar excess return is +1.5% with t=0.63 over 251 non-overlapping cases, and the forecast>2.5 bucket gives +1.45% with t=0.59 over 242 cases. A larger forecast does not earn more: the four entry-forecast quartiles average a gross gain of 6.2%, 4.3%, 2.3% and 7.8% per trade.
- F4: The edge sits where the 60-bar trend is also up.
- F5: Keeping only active days with a positive 60-bar return cuts the mean drawdown per window from -23.7% to -14.2%, while the annualised mean falls only from 0.38 to 0.29.
