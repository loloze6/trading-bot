---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's volatility over the past 20 days relative to its own usual level, the higher its return over the next day.
Consequence: A trader would lean long in a coin whose recent volatility is unusually high and refuse long trades in one that has gone unusually quiet.
Why:
- F2: A coin's next-day excess return rises steadily with its own 20-day volatility quintile: −0.20 % (t −4.12), −0.13 % (t −2.32), +0.00 %, +0.14 % (t 1.49), +0.19 % (t 2.23), each quintile about 6150 bars.
- F4: Five-day extremes show the same U shape. By decile of the 5-day move over its volatility, the next-day excess was +0.25 % for the lowest decile (t 2.20) and +0.33 % for the highest (t 2.80). Middle deciles ran down to −0.20 % (t −2.30).
