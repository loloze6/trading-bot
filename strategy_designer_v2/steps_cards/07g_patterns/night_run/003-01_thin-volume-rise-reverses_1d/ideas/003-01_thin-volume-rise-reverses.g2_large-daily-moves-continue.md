---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses
line: 7.g patterns
backtest: 003-01_thin-volume-rise-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day return in units of its 20-day return volatility, the higher its return over the next 5 days, in the direction of that day's move.
Consequence: A trader should avoid shorting a coin after its unusually large up days, since those days are followed by further gains.
Why:
- F1: The tested short fought a continuation. The top quintile of one-day moves in 20-day volatility units was followed by a mean excess 5-day return of +0.0160 (t 3.31, n 598, non-overlapping 5-day grid). On up days only, the largest-rise quartile gave +0.0180 (t 2.91, n 356), and the rise's size ranked positively with the excess 5-day return (Spearman rho 0.080, p 0.0026, n 1422). The effect held in both halves: 2018-2021 gave +0.0261 (t 3.42, n 256) and 2022-2025 gave +0.0085 (t 1.36, n 342).
- F4: The book sat short at a near-constant size, regardless of how large the rise was. Its mean position on active up days ran −0.40, −0.34, −0.36 and −0.33 across the rise quartiles, so it was fully exposed to the continuation in F1. Its daily mean return was negative or about zero on every coin (BTC −0.00050, ETH −0.00046, XMR −0.00044), and its Sharpe was −0.54.
