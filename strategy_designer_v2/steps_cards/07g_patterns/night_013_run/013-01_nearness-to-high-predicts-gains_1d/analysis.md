---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains_1d
idea tested: 013-01_nearness-to-high-predicts-gains
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3639 USD
---
## Findings
- **F1:** The forecast does not grade the 30-day outcome: the pooled slope of each coin's 30-bar excess return on the forecast has t = 0.95 (n = 526 non-overlapping cases), the quintile means are not monotone (-0.027, -0.031, +0.080, -0.013, -0.008 from the lowest to the highest forecast), and the per-coin t ranges from -1.48 (XRP) to 1.88 (BTC).
- **F2:** The book adds almost nothing beyond holding: mean daily return is 0.0001 against 0.0012 for holding, Sharpe is 0.52 against 0.58, the position is near flat on average (0.017, long 37% of bars and short 36%), and the book's yearly mean is below holding's in every year where the coins rose (2019, 2020, 2021, 2023, 2024, 2025).
- **F3:** Saturday stands out. The coins' mean Saturday return is 0.0044 (t = 5.39, n = 2416), against -0.0018 to +0.0032 on the other weekdays. Saturday minus the other days is positive in 7 of 8 years (t up to 3.06 in 2019, -1.24 in 2023) and in all 6 coins (t 0.34 for BTC to 2.67 for LTC).
- **F4:** Short-term momentum over 7 days looks significant in OLS but does not hold up. The 7-day excess return regressed on the vol-scaled 7-day past return gives t = 3.46 (n = 1958), but the Spearman rho is 0.005. After winsorising, the raw 7-day past return gives t = 1.07 (n = 2238). The median excess return is not monotone across quintiles. By year, t runs from -1.78 to 2.70. The effect is carried by a few large moves, mostly in XRP (t 2.95) and ZEC (t 2.07).
- **F5:** Relative volume against the 30-day average shows a 30-day OLS slope with t = 4.45 (n = 386), but the Spearman rho is only 0.052, so this is also outlier-driven. Signed volume (direction times log relative volume) has no slope at either horizon (t = 0.07 at 7 days, 0.48 at 30 days).
- **F6:** Volatility level does not order the 7-day excess return: quintile means go from -0.003 to +0.007 with no trend (OLS t 1.41 at 7 days, -0.78 at 30 days).

## Ideas
- No ideas: The only pattern that stands out after this many looks is the Saturday effect (F3). It is a calendar condition with no gradation, so it cannot be written as a graded idea, and the graded candidates (F4, F5) disappear under rank or winsorised measures.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
