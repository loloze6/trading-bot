---
line: 7.d not profitable
backtest: 012-01_liquidation-flush-rebound_1d
idea tested: 012-01_liquidation-flush-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3477 USD
---
## Findings
- **F1:** The book is long only on the flush bar itself and the rebound comes later, so it misses it: the mean allocation is 0.93 on the flush bar and 0.02 on the next bar, trades last 1.03 days, and the first day after a flush returns -0.0002 over the coin's mean (t -0.05, n 163); trades net -0.23% on average (t -0.44, n 160), giving a Sharpe of -0.03 and a Calmar of -0.02.
- **F2:** The rise after a flush shows on the second and third days: excess daily returns are 0.0086 (t 1.63) and 0.0093 (t 1.89) on days 2 and 3, against -0.0002 on day 1 and -0.0007 and -0.0026 on days 4 and 5 (n 163); from the next day's close to three days on, flush bars gain 0.0170 over the coin's mean (t 2.01, n 117).
- **F3:** The situation is too rare for the book to work: trades per bar are 0.0091, and the book holds a position on only 321 of 17524 coin-days.
- **F4:** Across all falls of at least one usual move (n 1642), the 3-day excess return grows with the volume burst: by volume-ratio quartile it is -0.0040, 0.0027, 0.0002 and 0.0188, and the top quartile (mean ratio 3.06, n 411) holds most of the gain (Spearman 0.053).
- **F5:** The long lower wick works against the rebound rather than for it: across the same falls, the 3-day excess return falls from 0.0141 in the shortest-wick quartile to -0.0002 in the longest (Spearman -0.072).
- **F6:** The forecast's size does not grade the outcome: 3-day excess returns by forecast tercile are 0.011, 0.030 and 0.013, and the Spearman correlation is -0.009, so the wick part of the forecast dilutes the volume part.

## Ideas
- `012-01_liquidation-flush-rebound.d1_delayed-flush-rebound-days-two-three` (from F1, F2, F6): When a bar closes sharply lower on volume far above its own 30-day average volume and leaves a long lower wick below its close, price rises over the second and third days after it, from the next day's close to three days after the flush; the more extreme the volume burst, the larger that rise.
- `012-01_liquidation-flush-rebound.d2_heavy-volume-fall-rebound` (from F3, F4, F5): When a coin's daily close falls by at least its usual 20-day move on volume far above its own 30-day average volume, price rises over the next 3 days; the larger the volume over its 30-day average, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
