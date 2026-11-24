---
line: 7.g patterns
backtest: 031-02.b1.b2.b1_failed-rally-longer-horizon_1d
idea tested: 031-02.b1.b2.b1_failed-rally-longer-horizon
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4830 USD
---
## Findings
- **F1:** The strongest pattern in the bars is that quiet coins outran busy ones over 40 days: the mean 20-day high-low range had a slope of −0.74 usual-moves with t −2.39, and 20-day volatility −0.60 with t −1.99 (459 cases on 45 days), with the calmest fifth beating its drift by +10.6 % and the two busiest fifths trailing by −10.2 % and −6.7 %. It does not stand out after about fifty tests, though: the same slope is t 0.14 at 20 days and −0.84 at 60 days, and the calm fifth did worse than the busy fifth in 2018 (−34.0 % vs −13.2 %), 2019 (−22.3 % vs −15.6 %) and 2022 (−14.6 % vs −8.3 %).
- **F2:** Nearness to the yearly low grades 40-day moves against the idea's side but cannot be told from chance: Spearman 0.137 (p 0.011, 344 cases), the per-day slope is t 0.90 (54 days), the farthest-from-low fifth averages −12.1 % against drift (t −1.78), and the nearest fifth −1.4 % (t −0.07); at 5, 10, 20 and 60 days the slope t stays between 0.44 and 0.84.
- **F3:** The book's gain is mostly the market's rise rather than its forecast: long bars (16,854) earned 3.58 bp each before costs, short bars (4,749) only 0.83 bp, and no coin's book mean daily return reached the coin's own (for example SOL 5.86 bp vs 33.50 bp, ADA 2.27 bp vs 23.14 bp).
- **F4:** Past 5-, 10-, 20- and 40-day returns forecast nothing reliable at 5 to 60 days: the largest per-day t is 1.80 (top 10-day-return fifth at 10 days, +2.48 %) and 1.54 (5-day return slope at 60 days on 19 days), with signs that flip between horizons (5-day return slope −0.21 at 20 days, +0.37 at 40 days).
- **F5:** Weekday shows no reliable effect on 10-day moves: Thursday starts average +0.218 usual moves (t 1.82, 407 cases) and every other weekday sits within |t| 0.6.

## Ideas
- No ideas: Across nearness to the yearly low, past returns over 5 to 40 days, volatility and range over 10 to 40 days, volatility ratio, weekday, year and coin group, at horizons from 5 to 60 days, nothing stood out beyond t 2.4. That is below what about fifty tests require, and the best pattern (F1) vanishes at the neighbouring horizons and reverses in three of eight years.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
