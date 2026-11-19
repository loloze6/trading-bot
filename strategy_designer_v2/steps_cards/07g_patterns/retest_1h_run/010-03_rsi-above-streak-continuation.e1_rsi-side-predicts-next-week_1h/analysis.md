---
line: 7.g patterns
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h
idea tested: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3080 USD
---
## Findings
- **F1:** The book's losses come from trading costs, not from a wrong forecast: before costs the position gains 0.00155 a day on BTC and 0.00199 a day on ETH, but fees take 0.00410 and 0.00366 a day. Allocation changes larger than 0.2 make up 88% of all fees (47,264 bars), and the book's mean daily return is negative on every weekday except Monday (t from -1.8 to -3.5).
- **F2:** Over 1 day, a coin's move tends to reverse, and the effect sits in high volatility. Its volatility-scaled 24-hour return against the next 24 hours' excess return has a correlation of -0.031 (t -2.34, 5,744 non-overlapping cases). The top past-24h quintile is followed by -0.0021 and the bottom by +0.0022. In the highest tercile of 7-day volatility the correlation is -0.102 (n 1,915, t ≈ -4.5). In the lowest tercile it is +0.052.
- **F3:** Over longer spans, moves tend to continue. The 72-hour scaled return against the next 72 hours has a correlation of +0.051 (t 2.20, 1,860 cases). The 168-hour return against the next 168 hours has +0.062 (t 1.73, 766 cases). BTC and ETH have the same sign at both horizons.
- **F4:** The tested forecast sorts 7-day excess returns at its extremes. The top forecast quintile is followed by +0.0174 (t 1.82) and the bottom by -0.0119 (t -1.24). Both coins show the ordering: BTC +0.0120 vs -0.0071, ETH +0.0228 vs -0.0168.
- **F5:** Calendar effects are weak once you allow for the many angles checked. Daily coin returns are highest on Wednesday (+0.0037, t 2.47, n 826) and lowest on Thursday (-0.0026, t -1.61), and the book's gain before costs shows no clear hour pattern.

## Ideas
- `010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week.g1_high-volatility-one-day-reversal` (from F2, F5): When a coin's recent 7-day volatility is high, the larger its 1-day return relative to that volatility, the more its return over the next 1 day runs the other way.
- `010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week.g2_three-day-volatility-scaled-continuation` (from F3, F4, F1): The larger a coin's 3-day return relative to its recent volatility, the higher its return over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
