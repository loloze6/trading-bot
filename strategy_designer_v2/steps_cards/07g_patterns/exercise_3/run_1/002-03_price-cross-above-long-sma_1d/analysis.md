---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3531 USD
---
## Findings
- **F1:** The vol-target book's gain does not come mainly from the 200-day-SMA situation. Forecast>0 grid bars gave a 20-day excess return of 0.0052 against −0.0002 when flat (Welch t 0.27, n 399 vs 412), and distance quintiles gave no ordered pattern (top quintile +0.0316, t 0.89; fourth quintile −0.0199, t −1.35).
- **F2:** The book's timing part was larger than its market part only in BTC (0.000669 vs 0.000531 per day) and was negative in XMR (−0.000376). All of its gain sits in trades of about 63 days (mean +35.7 %, 69 % winners), while trades shorter than 7 days lose (−5.8 % and −3.6 %, 3–14 % winners). The edge is a few long holds, not many entries.
- **F3:** Volatility changes how a day's move carries into the next 5 days. A day's return scaled by its 20-day volatility has a Spearman correlation with the next 5-day excess return of +0.093 in the lowest volatility tercile (n 929, about t 2.8) and −0.057 in the highest (n 929, about t −1.7), a gap of about 3.2 in Fisher z.
- **F4:** Pooled over all volatility, the scaled 1-day move rises roughly in order into the next 5-day excess return, from −0.0063 at −1.5 to −0.5 to +0.0159 above +1.5 (t 1.67, n 181). The per-coin Spearman correlations range only from −0.021 to +0.071, so the pooled slope is weak.
- **F5:** The weekday pattern does not hold up, and I count it as chance after this many angles. Friday's pooled excess is +0.00298 (t 3.66) and Wednesday's is −0.00304 (t −2.75), but the per-coin Friday-vs-rest t ranges from 0.34 to 2.53. Friday turns negative in 2018, 2022 and 2023 (t −0.42, −0.31, −1.10), and the pooled t counts the same dates once per coin.
- **F6:** The other non-monotone dips are also not graded effects. The second quintile of the 1-day return (t −3.70) and of the 20-day return (t −3.27) on the 5-day excess are isolated dips with flat neighbours, so I count them as noise from the many cuts examined.

## Ideas
- `002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation` (from F3, F4): In a coin whose 20-day volatility of daily returns is low, a day's return that is large relative to that volatility is followed by a move the same way over the next 5 days. The larger the scaled move, the larger the follow-through, and the effect weakens or reverses as the 20-day volatility rises.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
