---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-01_liquidation-flush-rebound
line: 7.d not profitable
backtest: 012-01_liquidation-flush-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a bar closes sharply lower on volume far above its own 30-day average volume and leaves a long lower wick below its close, price rises over the second and third days after it, from the next day's close to three days after the flush; the more extreme the volume burst, the larger that rise.
Consequence: A trader who sees a flush should expect the rebound a day later, not on the first day, and should hold through the third day.
Why:
- F1: The book is long only on the flush bar itself and the rebound comes later, so it misses it: the mean allocation is 0.93 on the flush bar and 0.02 on the next bar, trades last 1.03 days, and the first day after a flush returns -0.0002 over the coin's mean (t -0.05, n 163); trades net -0.23% on average (t -0.44, n 160), giving a Sharpe of -0.03 and a Calmar of -0.02.
- F2: The rise after a flush shows on the second and third days: excess daily returns are 0.0086 (t 1.63) and 0.0093 (t 1.89) on days 2 and 3, against -0.0002 on day 1 and -0.0007 and -0.0026 on days 4 and 5 (n 163); from the next day's close to three days on, flush bars gain 0.0170 over the coin's mean (t 2.01, n 117).
- F6: The forecast's size does not grade the outcome: 3-day excess returns by forecast tercile are 0.011, 0.030 and 0.013, and the Spearman correlation is -0.009, so the wick part of the forecast dilutes the volume part.
