---
line: 7.g patterns
backtest: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins_1d
idea tested: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4359 USD
---
## Findings
- **F1:** A daily close above the prior 20-day high was followed by the coin rising more than its normal drift. Over the next 5 days the excess was +3.11 % (t 2.18, 336 non-overlapping cases, strength 0.207), against −0.15 % (t −1.02, 6,934 cases) on all other grid days. Over the next 10 days it was +6.63 % (t 2.92, 190 cases), and 13 of the 19 coins showed a positive 5-day mean after breakouts.
- **F2:** The breakout continuation in F1 is not stable over time. It was +9.30 % (t 2.07, 93 cases) up to 2021 and only +0.74 % (t 0.79, 243 cases) from 2022. Its grading by how far the close sat above the 20-day high, in units of 20-day volatility, is weak and not monotonic: terciles −1.22 %, +7.51 %, +3.04 %; Spearman 0.105, p 0.055, 336 cases.
- **F3:** On the full 5-day grid, the brief's failed breakouts showed no downward follow-through that stands out from chance. A close back inside the range gave −0.52 % (t −0.60, 159 cases), and a close below the breakout day's low gave −0.73 % (t −0.61, 87 cases), against +0.02 % (t 0.13, 7,024 cases) on other days.
- **F4:** Being near the top of the range pointed the same way as F1. The top quintile of each coin's distance to its 20-day high gave +1.07 % over 5 days (t 2.21, 1,213 cases), and the top quintile of its 20-day return gave +1.03 % (t 2.01, 1,213 cases). The middle quintiles were negative: distance-to-high quintile 2 gave −0.68 % (t −2.14), and 20-day-return quintile 1 gave −0.81 % (t −2.74).
- **F5:** Weekday patterns are large but cannot count as evidence, because the 19 coins move together on the same calendar days, which inflates these t's.
- **F6:** The book earned only from coins falling while it was short. On its 761 active coin-days it made +0.13 % a day while the coins moved −0.70 %, with a correlation of −0.70 between the two. Its yearly mean daily returns stayed within ±0.02 %, never moving with the coins' own yearly drift (−0.35 % to +0.58 %).

## Ideas
- `029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins.g1_breakout-closes-keep-rising` (from F1, F2, F4, F3): When a coin closes above its prior 20-day high, it keeps rising over the next 10 days. The further that close sits above the old high, measured against the coin's 20-day volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
