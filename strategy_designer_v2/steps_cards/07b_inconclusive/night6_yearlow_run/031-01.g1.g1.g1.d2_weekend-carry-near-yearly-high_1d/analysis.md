---
line: 7.b inconclusive
backtest: 031-01.g1.g1.g1.d2_weekend-carry-near-yearly-high_1d
idea tested: 031-01.g1.g1.g1.d2_weekend-carry-near-yearly-high
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3493 USD
---
## Findings
- **F1:** The tested slope is on the predicted side but weak and not graded. Across forecast quintiles the mean excess weekend return runs +0.84 %, +0.13 %, +0.93 %, +1.03 %, +1.09 % (forecast means 3.4 to 19.8; t 1.66, 0.37, 2.47, 2.34, 1.70; 211 cases each). The level sits well above zero in every quintile, but nearness to the yearly high barely moves it, which is why the step-5 slope is 0.00045 with t 0.99 over 1192 cases on 317 Fridays.
- **F2:** What lifts these weekends is the prior rise itself, not nearness to the high. On all Fridays, those with a positive 14-day return earn an excess 2-day return of +0.81 % (t 3.08, 1055 cases, 281 days), and those with a negative one earn −0.35 % (t −1.20, 1057 cases). The excess return on the 14-day return has a slope of 0.039 (day-clustered t 2.89, 2112 cases, 362 days).
- **F3:** The effect grows with the size of the rise.
- **F4:** The pull of the 14-day return is specific to the bars that lead into the weekend. Its clustered slope is 0.054 (t 3.36) from Thursday and 0.039 (t 2.89) from Friday. It is −0.002 to 0.021 (t −0.13 to 1.21) from Monday to Wednesday and −0.015 to −0.022 (t −1.11, −1.25) from Saturday and Sunday. Over all non-Friday bars it is 0.0047 (t 0.66, 12692 cases).
- **F5:** The Friday 14-day-return slope is positive in 5 of 6 coins (BTC 0.030, ETH 0.046, LTC 0.027, XRP 0.045, ZEC 0.048; t 1.4 to 2.9; XMR 0.009, t 0.34) and in 7 of 8 years (2023 −0.017, t −0.62). The tested idea's own cases are positive in every coin (+0.23 % to +1.22 %) and in 7 of 8 years (2022 −0.22 %). The effect is spread across the data, but too small per subgroup to stand out.
- **F6:** The tested idea's size is clear even though its slope is not. The unusual move is +0.85 % per case (t 3.27, 315 days), 0.127 of a usual 2-day move. The total move is +1.11 %, 5.7 times the 0.19 % cost of a trade, and the book's Sharpe is 1.13.

## Ideas
- `031-01.g1.g1.g1.d2.b1_weekend-carry-near-high-more-coins` (from F1, F5, F6): After a two-week rise, the closer a coin's Friday close (UTC) is to its highest price of the past year, the more it rises over the following Saturday and Sunday together.
- `031-01.g1.g1.g1.d2.b2_two-week-rise-weekend-carry` (from F2, F3, F4, F5): The larger a coin's 14-day return at its Friday close (UTC), the more it rises over the following Saturday and Sunday together.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
