---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Saturday is followed over Monday and Tuesday by a move in the same direction that grows with the size of Saturday's move scaled by the coin's 30-day volatility of hourly returns, while that volatility is low against its own past year, whichever way the coin's 7-day return points.
Consequence: A trader would follow Saturday's move into Monday and Tuesday in calm markets without waiting for the week to agree, which roughly doubles the cases available to the tested book.
Why:
- F1: Saturday's volatility-scaled return predicts the volatility-scaled return over Monday and Tuesday in the same direction (slope 0.211, t 6.27, 2103 Mondays), and this holds in both halves of the period (2018–2021 t 4.77, 2022–2025 t 3.97). On the other start days, the return from two days back predicts nothing comparable (t between −1.18 and 2.11).
- F2: The book's condition that the 7-day return agree with Saturday is not what carries the effect, and calm markets are where it is largest.
