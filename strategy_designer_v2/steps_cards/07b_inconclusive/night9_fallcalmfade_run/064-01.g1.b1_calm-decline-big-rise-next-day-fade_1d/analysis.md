---
line: 7.b inconclusive
backtest: 064-01.g1.b1_calm-decline-big-rise-next-day-fade_1d
idea tested: 064-01.g1.b1_calm-decline-big-rise-next-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2189 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but too small for this data to show. The mean unusual next-day move of the short bets is +0.29 % with t 1.00 over 321 cases on 201 days. Its strength is 0.057 of the coin's usual 4.73 % daily move, close to the 0.05 that real ideas have shown so far. At that strength the test would need about four times as many distinct days to reach t 2.
- **F2:** In folds B and C the same cases (188 cases, 108 days) give a next-day unusual move of +0.58 % with t 1.31, and 56 % of them are positive. So the one-day fade is weak but consistently on the predicted side, not reversed.
- **F3:** The effect exists only at the plan's one-day horizon. The unusual move is −0.02 % (t −0.03) over 2 days, +0.24 % (t 0.27) over 3 days, +0.24 % (t 0.24) over 5 days and +0.94 % (t 0.60) over 10 days. The test measured it at the right horizon.
- **F4:** The fade is not graded by the rise's size at one day, though step 5's median split passed (+0.50 %).
- **F5:** The effect is uneven across years and coins.
- **F6:** The book cannot pay at this size. The total move per case is +0.16 %, which is 0.8 times the 0.19 % cost of a trade. The book's Sharpe is −0.03 and it is in a position on 4 % of coin-days, so its result reflects the effect's small size rather than the holding or sizing.

## Ideas
- `064-01.g1.b1.b1_calm-decline-fade-more-coins` (from F1, F2, F3): In a falling, calm market, a coin's one-day rise that is large against its 20-day daily swing is given back over the next day, and the larger the rise in those swing units beyond about one usual daily move, the larger the fall that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
