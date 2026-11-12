---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is above its 200-day average and also above its close of 20 bars earlier, the coin keeps rising over the next 20 bars by more than its average 20-bar return.
Consequence: Take or hold the long only while the price is above the long average and the past month's move is up; refuse it when the price is above the average but sliding.
Why: F4: Above the SMA, the direction of the last 20 days decides the result. On bars with a positive forecast where the close is below its level 20 bars earlier (3701 bars), the gross daily return is −0.000674 and the next-20-bar return is −0.0018. Where it is above (4647 bars), these are +0.004210 and +0.0603.; F2: Being above the SMA alone adds almost nothing over being below it. Bars with a positive forecast return 0.001337 the next day and 0.0322 over 20 bars, against 0.001239 and 0.0260 for flat bars. The book's gross daily gain (0.001023) is below simply holding the coins (0.001287), which is why the book's Sharpe trails holding's Sharpe by −0.065.; F5: The losses cluster in the bear years. The gross daily return is −0.000691 in 2018 and −0.000362 in 2022, when the book was long on only 19% and 10% of bars. In 2023 the book lost −0.000198 a day while the coins gained +0.001502. These failed entries during declines drive the poor Calmar of 0.14.
