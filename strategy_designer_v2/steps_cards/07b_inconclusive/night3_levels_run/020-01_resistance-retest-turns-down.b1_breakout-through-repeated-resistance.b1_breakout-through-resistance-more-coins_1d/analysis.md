---
line: 7.b inconclusive
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins_1d
idea tested: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4046 USD
---
## Findings
- **F1:** The tested breakouts show no rise beyond the coin's normal drift at the plan's 10-day horizon (+0.19 % per case, t 0.52, 2632 cases, mean strength 0.010). The verdict's numbers are similar: +0.08 %, t 0.23, 2613 cases, strength 0.005. This test already used all 19 coins on all four folds, so there is no more data to add.
- **F2:** The rise after a breakout is concentrated in the first 3 days. The unusual move is +0.13 % at 1 day (t 1.29), +0.47 % at 3 days (t 2.76, 2757 cases), +0.28 % at 5 days (t 1.09), +0.19 % at 10 days (t 0.52) and +0.26 % at 20 days (t 0.44). The 10-day test therefore measured the idea after its move had mostly faded. The 3-day move is about 2.1 times the 0.22 % cost of a buy and a sell.
- **F3:** At 10 days, the outcome of a breakout follows the coin's prior 30-day return. Breakouts in the lowest quarter of 30-day return average −2.94 % (t −3.29, 305 cases); those in the highest quarter average +2.85 % (t 2.69, 520 cases).
- **F4:** Within each 30-day-return quarter, breakouts do no better than all grid bars of the same quarter. The differences, breakouts minus grid bars, are −1.74 % (Welch t −1.66), +0.66 % (t 0.74), +1.44 % (t 1.62) and +0.22 % (t 0.15). At 10 days the level crossing adds nothing that the coin's 30-day return does not already carry.
- **F5:** On all grid bars, the 10-day unusual move rises with the 30-day return. Grid bars with a positive 30-day return average +1.14 % (t 2.04, 1314 cases) and those with a non-positive one average −1.39 % (t −3.62, 1314 cases). The rank correlation between the 30-day return and the 10-day strength is 0.044 (p 0.025, 2628 cases). The top quarter's +2.63 % is about 12 times the cost of a trade.
- **F6:** The 10-day effect swings with the market's year and is not stable. By year, the unusual move per case is −3.6 % in 2018 (t −2.0), −3.7 % in 2022 (t −4.5) and −2.2 % in 2025 (t −3.3), against +1.9 % in 2023 (t 2.8) and +2.7 % in 2024 (t 3.3). No coin reaches |t| 1.2.
- **F7:** The touch-count grading points the idea's way but is small. Cases with N ≥ 3 beat cases with N ≤ 2 by 0.37 % at 10 days. Cases with the largest forecasts (top three quarters) average +0.52 % (t 1.22), against −0.82 % (t −1.30) for the lowest quarter.

## Ideas
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise` (from F2, F1, F7): When a coin closes above a price where it turned down several times in the past 90 days, having closed below it the day before, it tends to rise over the next 3 days, and the more times it turned down there before, the larger the rise.
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation` (from F3, F4, F5): The larger a coin's 30-day return, the larger its rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
