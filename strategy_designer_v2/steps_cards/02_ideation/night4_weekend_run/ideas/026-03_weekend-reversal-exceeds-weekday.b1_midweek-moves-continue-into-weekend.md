---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday
line: 7.b inconclusive
backtest: 026-03_weekend-reversal-exceeds-weekday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 48-hour return over Wednesday and Thursday is followed by a move in the same direction over the next two days, Friday and Saturday, and the larger the Wednesday-Thursday move, the larger the move that follows.
Consequence: A trader would follow a coin's midweek move into the weekend rather than fade it, with more conviction the larger the move.
Why:
- F2: The main measure's positive difference (+0.031, Welch t 0.84) comes from the weekday comparison group, not from the weekend. Friday-ending cases have a reversal score of -0.069 (t -2.19), and their next 48 hours follow the past 48 hours with slope +0.056 (t 3.38, 2392 cases), which is momentum. Comparing Monday with all Tuesday-to-Friday cases leaves a difference of only 0.025 (Welch t 0.77).
- F5: The Friday continuation of the Wednesday-Thursday 48-hour move is strongest in 2018 (slope 0.156, t 4.12), 2022 (0.189, t 3.11) and 2025 (0.169, t 3.88). It is negative in 2019 (-0.112, t -1.98), 2020 (-0.064) and 2023 (-0.062). It is positive in 5 of 6 coins (ZEC 0.138, t 3.53; ETH 0.092, t 2.40) and negative only in XMR (-0.035).
- F6: Per case the tested book's total move is -0.26 % over 48 hours against a trade cost of 0.19 %, on a usual 48-hour move of 6.56 %. A move one usual size large with F2's slope of 0.056 would carry about 0.37 %, roughly twice the cost.
