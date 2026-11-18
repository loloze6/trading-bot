---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on
line: 7.d not profitable
backtest: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises over one day by more than its usual daily move (its 20-day volatility), it keeps rising over the next 5 days, only while the coin's own 60-day return is positive. The larger the rise in units of that volatility, the larger the further rise.
Consequence: Follow sharp up days only in a coin that is itself trending up, and refuse them in a falling coin.
Why:
- F5: The book misses the market's rise. Its mean position is 0.23 and it is long on only 43% of bars, while the coins rose +0.12% a day on average. Every coin's book mean daily return (-0.068% to +0.036%) is far below its coin's (+0.067% to +0.155%), so Sharpe minus holding's Sharpe is -0.72.
- F6: The carry on days 2 to 5 depends on the market's direction. Their mean excess return after rises was -1.44% in 2018 and -0.88% in 2022, against +1.98% in 2020 and +0.87% in 2021.
