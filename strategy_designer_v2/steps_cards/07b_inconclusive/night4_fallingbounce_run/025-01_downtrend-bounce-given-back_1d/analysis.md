---
line: 7.b inconclusive
backtest: 025-01_downtrend-bounce-given-back_1d
idea tested: 025-01_downtrend-bounce-given-back
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3751 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar: the 1324 short cases show a mean short-direction unusual 5-day move of +0.48 % (t 1.81), 0.048 of the coin's usual 5-day move (10.60 %), which is the size real ideas usually have; my own recount (1361 cases) gives +0.54 % with t 2.01, so the result sits right at the threshold.
- **F2:** The effect is mixed across periods and coins. The 5-day unusual move is strongly positive in 2018 (+2.37 %, t 2.83, 255 cases), 2019 (+1.48 %, t 2.47) and 2025 (+1.58 %, t 2.53). It is negative in 2020 (-2.18 %, t -2.33) and 2021 (-2.08 %, t -1.80). Five of six coins are positive (ETH +1.20 %, ZEC +1.10 %, LTC +0.92 %, BTC +0.89 %, XMR +0.29 %). XRP is negative (-1.20 %, t -1.43). With six coins, this spread is what keeps the t below 2.
- **F3:** The grading the idea predicts runs the wrong way among the cases. The smallest quarter of |forecast| fades +1.35 % over 5 days (t 2.64, 341 cases) and the largest quarter -0.54 % (t -0.90). By the raw scaled rise, the smallest quarter (mean 0.52 usual moves) fades +1.56 % (t 2.93) and the largest (mean 1.93) only +0.23 % (t 0.38). This matches the failed supporting check (larger half minus smaller half -0.69 %).
- **F4:** The contrast the brief names does show. On the non-overlapping 5-day grid, rises above 1 usual daily move are followed by a short-direction unusual move 2.63 % larger in falling coins than in coins whose 90-day return is not negative (Welch t 2.35; 170 against 244 cases).
- **F5:** In coins whose 90-day return is not negative, large one-day rises are followed by further rises that grow with the size of the rise. Measured as the 5-day unusual move in the short direction on the grid:
- **F6:** The fade is drowned by the coins' own rise. The normal drift in the short direction is -0.59 % per 5 days, which leaves a total move of -0.11 % per case, -0.6 times the 0.19 % cost of a trade. Across all falling-regime grid bars, the unusual move is only +0.03 % (t 0.12, 1507 cases).

## Ideas
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins` (from F1, F2): In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the larger that rise in units of the usual daily move, the larger the fall.
- `025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising` (from F4, F5): In a coin whose 90-day return is not negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, and the larger that rise in units of the usual daily move, the larger the rise that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
