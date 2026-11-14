---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 60-day and 20-day returns are both positive, its next few days' returns are higher than its average daily return, so the continuation shows up at a short horizon rather than over the following 20 days.
Consequence: A trader can hold a coin long over the next days while both its slow and fast returns are up, and stay flat otherwise, to collect short-horizon continuation and avoid its falling stretches.
Why:
- F1: Almost all of the book's gain came from days when both the 60-day and the 20-day return were up. Those 3,047 coin-days carried 9.23 of the 13.11 summed daily book return, with a book mean of 0.003028 and a coin mean of 0.003821. Every other state had a book mean near 0 (between −0.000036 and −0.000012), and the 60-up/20-down state had a negative coin mean of −0.001731.
- F2: The book earns from timing more than from the market's own rise. Of its mean daily return of 0.000754, only 0.000252 is exposure times the coin's drift and 0.000553 is timing (t 3.64), at a mean allocation of 0.21. The coin rose 0.002937 a day while held against 0.000311 while flat (n 5,816 vs 11,564; Welch t 3.21), even though the plan's 20-bar excess return was not significant (mean 0.019, t 0.85, 269 blocks).
- F5: Much of the edge over holding comes from staying out of falling years. In 2018 the book's daily mean was −0.00019 against the coins' −0.00347, and in 2022 it was −0.00032 against −0.00180, with only 16% of days held in each. In strongly rising years the book lagged holding, for example 2021 at 0.00047 vs 0.00409.
