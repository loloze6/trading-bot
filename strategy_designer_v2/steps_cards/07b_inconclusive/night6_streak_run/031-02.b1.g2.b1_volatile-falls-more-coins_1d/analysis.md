---
line: 7.b inconclusive
backtest: 031-02.b1.g2.b1_volatile-falls-more-coins_1d
idea tested: 031-02.b1.g2.b1_volatile-falls-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4046 USD
---
## Findings
- **F1:** The test looked two days ahead, but the rebound shows only on the first day after the fall. The slope of the excess return on the size of the fall has a day-pooled t of 2.96 over 1 day (17,931 down-day cases, 2,390 days), against 1.00 over 2 days (8,898 cases). Over 3, 5 and 10 days the t is 1.37, 2.12 and 1.55.
- **F2:** The second day adds nothing. The excess return from the close 1 day after the fall to the close 2 days after has a slope on the fall of 0.008 (t 0.16, 17,756 overlapping cases), so the 2-day test diluted a 1-day effect with a day of noise.
- **F3:** Over 1 day the rebound is graded and is carried by the deepest falls. Fall deciles 1 to 4 have excess returns of -0.02 % to -0.26 %. The top decile (mean fall 11.2 %) has +1.02 % (t 2.01, strength 0.124), which is about 4.6 times the 0.22 % cost of a trade. The slope stays at t 2.02 with the largest 1 % of falls removed.
- **F4:** Volatility grades the 1-day rebound as the idea says. The slope on the fall is 0.193 (t 2.22, 3,042 cases) in the highest third of 60-day volatility, against 0.023 (t 0.25) in the lowest third and 0.041 (t 0.43) in the middle third. The plan's product form (fall × volatility, 1-day t 1.73) measures this less well than the fall alone.
- **F5:** The 1-day effect is spread across the long-listed coins. ADA has t 4.44, ZEC 3.23, XMR 2.81, TRX 2.74, XRP 2.66, DOGE 2.41 and ETH 2.18. It is near zero or negative for AVAX, INJ, NEAR, SOL and TAO (t -1.53 to 0.13). It is strongest in 2020 to 2021 (t 2.73 and 2.75) and weaker since 2022 (t 0.33 to 1.09).
- **F6:** The tested 2-day result is on the predicted side but short of the bar: slope t 1.33, unusual move +0.03 % per case (t 0.14), strength 0.004. The test already used every coin and all four folds, so no more data is available to sharpen it at its own horizon.

## Ideas
- `031-02.b1.g2.b1.b1_volatile-falls-next-day-rebound` (from F1, F2, F3, F4, F6): The larger a coin's percentage fall on its latest day, the more it rises over the next 1 day, and this rebound is larger the higher the coin's volatility over the past 60 days.
- `031-02.b1.g2.b1.b2_deep-fall-next-day-rebound` (from F1, F3, F5): The larger a coin's percentage fall on its latest day, the more it rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
