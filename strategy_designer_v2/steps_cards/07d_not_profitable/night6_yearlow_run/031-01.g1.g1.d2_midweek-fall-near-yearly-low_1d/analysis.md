---
line: 7.d confirmed, not profitable
backtest: 031-01.g1.g1.d2_midweek-fall-near-yearly-low_1d
idea tested: 031-01.g1.g1.d2_midweek-fall-near-yearly-low
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4075 USD
---
## Findings
- **F1:** The book fails only on Calmar (0.42). Its deepest fall is -19.6 % against a yearly return of +8.1 %, built up from w5 through w10 (the window lows reach -13.1 %, -16.3 %, -17.6 %, -14.5 %, -19.6 % and -18.7 %). In w4–w10 the low-volatility shorts lost a summed 0.43 while the low-volatility longs gained 0.83.
- **F2:** The short side adds risk and no gain. The 680 mean_reversion short Saturdays earn +0.045 % per case (t 0.52, hit rate 48 %) and hold the worst single loss (-13.8 %). The longs earn +0.50 % (546 cases, t 5.5) in the lower half of the range and +0.60 % (449 cases, t 3.5) in the upper half. Removing all shorts lifts the book from Calmar 0.42 to 1.03, the deepest fall from -19.6 % to -9.0 % and Sharpe from 0.84 to 1.14.
- **F3:** The short side's loss sits entirely in the coin's quietest tercile of 20-day volatility, and it changes sign with volatility.
- **F4:** Inside volatility the short side is graded the way the idea says.
- **F5:** High volatility is not an effect of its own, so it can repair the idea.
- **F6:** Keeping the long side and dropping only the low-volatility shorts gives the best book. It has Calmar 1.16 (deepest fall -10.0 %, yearly +11.6 %) and Sharpe 1.19, against 1.03 and 1.14 with no shorts at all.
- **F7:** The short side lost money in 2019, 2021, 2023, 2024 and 2025 (summed -0.31, -0.12, -0.50, -0.46 and -0.33). The long side was positive in every year from 2018 to 2025. The long side is the stable part of the effect.

## Ideas
- `031-01.g1.g1.d2.d1_midweek-fall-volatile-yearly-low` (from F1, F3, F4, F5, F6): The higher a coin's return over the four days from Monday's close to Thursday's close, the more it rises over Saturday (UTC), and this grading does not come from Friday's own move. A Monday-to-Thursday fall is followed by a Saturday fall only while the coin trades in the lower part of its past-year range and its daily swings over the past 20 days are large against its own usual. The larger that fall and the wider those swings, the larger Saturday's decline.
- `031-01.g1.g1.d2.d2_midweek-gain-lifts-saturday` (from F1, F2, F7): The higher a coin's return over the four days from Monday's close to Thursday's close, the more it rises over Saturday (UTC), and this grading does not come from Friday's own move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
