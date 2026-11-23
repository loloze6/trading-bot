---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses_1d
idea tested: 030-03_heavy-flat-high-close-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.7183 USD
---
## Findings
- **F1:** On heavy-volume days (volume at least 2x the prior 20-day mean, 733 non-overlapping cases), a close near the high is followed by a rise over the next 5 days, the opposite of the tested reversal. The close-location terciles (mean 0.20, 0.55, 0.86) give strengths of 0.009, 0.095 and 0.160 (t 0.13, 1.28, 2.36). The top tercile's unusual move is +1.85 % (t 2.31) and its total move +2.47 % (t 3.09) over 244 cases. That is 13 times the 0.19 % cost of a trade.
- **F2:** The top-tercile result holds across coins and across the two halves of the record. It is positive in all six coins (BTC 0.237, ETH 0.024, LTC 0.104, XMR 0.088, XRP 0.369, ZEC 0.112). It is positive in both halves (w1–w12 0.178, t 2.08, n 127; w13–w24 0.139, t 1.31, n 117).
- **F3:** Heavy-volume days that come after a 5-day rise are followed by a further rise over 5 days. Their strength is +0.144 (t 2.67, n 388), their unusual move +1.65 % (t 2.50) and their total move +2.26 % (t 3.43). After a 5-day fall the strength is only 0.025 (t 0.41, n 345). The top tercile of the 5-day return gives 0.311 (t 4.07, n 245).
- **F4:** Among heavy-volume days after a 5-day rise, the follow-on grows with the volume. The volume-ratio terciles (mean 2.13, 2.54, 4.17) give strengths of 0.092, 0.096 and 0.243, and unusual moves of +1.08 %, +0.97 % and +2.90 %.
- **F5:** After a 5-day rise, the follow-on is positive in every coin: strengths 0.06 to 0.19 (XMR 0.062 lowest, ETH 0.190 highest). The two halves give 0.061 (t 1.04) and 0.233 (t 2.54).
- **F6:** Close location and a prior rise add up. Heavy-volume days after a 5-day rise that close in the top close-location tercile give a strength of 0.205 (t 2.75, n 194). Those in the bottom tercile give 0.045 (t 0.41, n 64).
- **F7:** The tested score, (close location − 0.5) × volume ratio, is only weakly graded on heavy-volume days. Its quintiles give −0.057, 0.082, 0.090, 0.162 and 0.163. The Pearson correlation is 0.077 (p 0.037) and the Spearman 0.039 (p 0.29).
- **F8:** Plain continuation in the direction of the 5-day move is not specific to heavy volume. Its strength is 0.064 (t 1.58, n 733) on heavy-volume days and 0.011 (t 0.56, n 2390) on below-average-volume days. The Welch t of the difference is 1.19. The effect sits on the up side only (F3).
- **F9:** The book lost on its trades: 289 short trades with a mean net result of −3.14 % and a median of −2.34 %. Its Sharpe is −0.50 and its yearly return −3.8 %.

## Ideas
- `030-03_heavy-flat-high-close-reverses.g1_heavy-volume-high-close-continues` (from F1, F2, F6, F7): On a day when a coin's volume is far above its 20-day average, the closer its close sits to the day's high, the more the coin rises over the next 5 days. The effect is larger the heavier that day's volume is.
- `030-03_heavy-flat-high-close-reverses.g2_heavy-volume-extends-rally` (from F3, F4, F5, F6, F8): On a day when a coin's volume is far above its 20-day average, the larger its 5-day return up to that day, the more it keeps rising over the next 5 days. The effect is larger the heavier that day's volume is.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
