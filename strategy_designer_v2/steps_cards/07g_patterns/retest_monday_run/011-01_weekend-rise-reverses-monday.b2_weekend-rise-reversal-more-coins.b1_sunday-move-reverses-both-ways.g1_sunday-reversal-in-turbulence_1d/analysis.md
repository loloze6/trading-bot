---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4755 USD
---
## Findings
- **F1:** The move of the UTC Saturday bar is reversed by the Sunday bar. The drift-removed next-day return, scaled by 20-day volatility, regressed on Saturday's return over its 20-day volatility gives slope −0.147 (t −6.56, 2616 cases); on raw returns the slope is −0.125 (t −6.48). No other weekday's next day reverses this strongly: Tuesday is −0.064 (t −2.48) and Sunday −0.054 (t −1.96).
- **F2:** Saturday's reversal is graded by the size of the move. Ranked into quartiles of |Saturday return / 20-day vol|, the next day's drift-removed return against the move averages +0.07 %, +0.03 %, +0.27 % (t 1.80) and +0.85 % (t 4.43), 654 cases each. The top quartile alone covers 3.9 times the 0.22 % cost of a trade.
- **F3:** Saturday's reversal holds across years and coins. Its slope is negative in 7 of 8 years (t ≤ −2 in 2018, 2019, 2022, 2023 and 2024, e.g. −0.240 with t −5.44 in 2024), with 2025 the exception (+0.067, t 0.90). It is negative in most coins (SOL −0.44 t −3.53, LTC −0.21 t −2.81, AAVE −0.26 t −2.58). It is gone after 2 days (slope +0.028, t 0.74), so it is a one-day effect.
- **F4:** The move of the UTC Wednesday bar continues, and the continuation grows with the horizon. The scaled slope is 0.065 (t 2.52) over 1 day, 0.215 (t 6.77) over 2, 0.242 (t 6.62) over 3 and 0.439 (t 9.00) over 5 days (2427 cases). On raw returns the 5-day slope is 0.304 (t 7.13). This is the strongest pattern of the roughly 28 weekday × horizon cells examined, and the opposite sign to Sunday's 5-day slope (−0.118, t −1.55).
- **F5:** Wednesday's continuation is robust and graded. The 5-day slope is positive in 7 of 8 years (t > 2 in 2018, 2021, 2022, 2023, 2024 and 2025; 2024: 0.84, t 6.33). It is positive in every coin shown (ADA 0.80 t 4.08, DOGE 1.03 t 4.23, LTC 0.57 t 3.83, ETH 0.56 t 3.31, BTC 0.48 t 2.92). The 5-day drift-removed move in the direction of Wednesday's move rises from +0.60 % in the smallest |move/vol| quartile to +2.90 % in the largest, about 13 times the cost of a trade.
- **F6:** Sunday's own move reverses over the next 2 days more strongly the lower Sunday's volume is against its 20-day average. By volume quartile, low to high, the scaled slope is −0.43 (t −3.11), −0.24 (t −1.91), −0.19 (t −2.10) and +0.07 (t 1.01), about 651 cases each. This is the brief's thin-liquidity prediction, which the tested idea did not use. Ranked by the 20-day/60-day volatility ratio instead, only the top quartile reverses (−0.26, t −3.24).
- **F7:** The book's profit is almost entirely Monday. Its mean daily return on Monday days is +0.221 % (std 1.79 %, 414 days), against +0.00 % to +0.01 % on Tuesday to Saturday and −0.03 % on Sunday. Long trades average +1.86 % net (3278 trades) and short trades −0.86 % (2963 trades), so the short side costs the book money.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence.g1_saturday-move-reverses-sunday` (from F1, F2, F3): A coin's UTC Saturday move is undone over the next 1 day (Sunday), and the larger Saturday's move relative to the coin's 20-day volatility, the larger the part that is undone.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence.g2_wednesday-move-continues-five-days` (from F4, F5): A coin's UTC Wednesday move continues in the same direction over the next 5 days, and the larger Wednesday's move relative to the coin's 20-day volatility, the larger the continuation.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence.g3_thin-volume-sunday-move-reverses` (from F6, F7): A coin's Sunday move is undone over the next 2 days (Monday and Tuesday), and the lower Sunday's volume stands relative to the coin's 20-day average volume, the larger the part that is undone.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
