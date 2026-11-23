---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's UTC Saturday move is undone over the next 1 day (Sunday), and the larger Saturday's move relative to the coin's 20-day volatility, the larger the part that is undone.
Consequence: A trader would lean against a large Saturday move for Sunday, and against a small one hardly at all.
Why:
- F1: The move of the UTC Saturday bar is reversed by the Sunday bar. The drift-removed next-day return, scaled by 20-day volatility, regressed on Saturday's return over its 20-day volatility gives slope −0.147 (t −6.56, 2616 cases); on raw returns the slope is −0.125 (t −6.48). No other weekday's next day reverses this strongly: Tuesday is −0.064 (t −2.48) and Sunday −0.054 (t −1.96).
- F2: Saturday's reversal is graded by the size of the move. Ranked into quartiles of |Saturday return / 20-day vol|, the next day's drift-removed return against the move averages +0.07 %, +0.03 %, +0.27 % (t 1.80) and +0.85 % (t 4.43), 654 cases each. The top quartile alone covers 3.9 times the 0.22 % cost of a trade.
- F3: Saturday's reversal holds across years and coins. Its slope is negative in 7 of 8 years (t ≤ −2 in 2018, 2019, 2022, 2023 and 2024, e.g. −0.240 with t −5.44 in 2024), with 2025 the exception (+0.067, t 0.90). It is negative in most coins (SOL −0.44 t −3.53, LTC −0.21 t −2.81, AAVE −0.26 t −2.58). It is gone after 2 days (slope +0.028, t 0.74), so it is a one-day effect.
