---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-01_strong-volatile-momentum
line: 7.g patterns
backtest: N3-01_strong-volatile-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily fall of more than 1.5 times the coin's recent daily volatility, the next day's return is above the coin's average, as a one-day bounce.
Consequence: A trader can avoid selling into the close of a sharp down day, or can buy it for a one-day hold.
Why:
- F5: After bars falling 1.5 to 2.5 recent volatilities in a day, the next day's excess return is +0.0044 (t=2.03, n=679). After falls beyond 2.5 volatilities it is +0.0059 (t=1.64, n=300). Up moves of the same size are followed by about -0.001 (t≈-0.5).
