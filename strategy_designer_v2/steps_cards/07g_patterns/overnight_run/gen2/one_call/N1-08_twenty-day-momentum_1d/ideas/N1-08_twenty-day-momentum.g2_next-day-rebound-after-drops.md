---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-08_twenty-day-momentum
line: 7.g patterns
backtest: N1-08_twenty-day-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close that falls at least one standard deviation of the coin's recent daily returns, the coin rises on the next day by more than on an average day.
Consequence: A trader can buy at the close of a large down day for a one-day hold, or avoid selling into it.
Why:
- F4: After a daily close at least 1 standard deviation down (scaled by 20-day volatility), the next day's excess return averages +0.56% (t=4.41, 1835 cases), against -0.07% (t=-1.72, 15545 cases) on all other days.
- F5: The next-day rebound after a 1-sd down day is positive in all six coins (XMR +0.99%, t=3.57, n=314). It holds both when the 20-day trend is down (+0.52%, t=3.12, n=1200) and when it is up (+0.65%, t=3.31, n=635). It is strongest in 2020 and 2021 (t=3.49 and 3.43) and absent in 2024 (t=-0.44).
