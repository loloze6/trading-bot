---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-01_strong-volatile-momentum
line: 7.g patterns
backtest: N3-01_strong-volatile-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily return on the day after a Thursday or Friday close is higher than its average daily return, because flows tied to the end of the week and the weekend lift spot crypto.
Consequence: A trader can time new longs to be held over the Thursday and Friday closes, and refuse to open them on Monday and Wednesday closes.
Why:
- F1: The next-day return after a bar's close depends on the weekday, measured as excess over the coin's mean on non-overlapping 1-bar returns. After Thursday bars it is +0.0026 (t=2.77, n=2483) and after Friday bars +0.0035 (t=4.44, n=2479). After Monday bars it is -0.0024 (t=-2.47, n=2490) and after Wednesday bars -0.0033 (t=-2.98, n=2489).
- F2: The Thursday/Friday excess is positive in 7 of 8 years and significant in four of them: 2019 t=5.38, 2020 t=3.46, 2023 t=2.43, 2024 t=2.55. Only 2022 is negative (t=-1.59). It is positive in all 6 coins, from BTC +0.0009 (t=0.90) to LTC +0.0056 (t=3.50).
