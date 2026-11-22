---
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation_1d
idea tested: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4148 USD
---
## Findings
- **F1:** The flatness factor adds nothing to the forecast. Splitting range position into a flat part and a trending part gives similar coefficients (flat 0.0122, t 1.55; trending 0.0065, t 1.34). The least flat fifth of 30-day ranges, mean flatness 0.085, is followed by the largest 5-day move above the coin's drift (+1.44 %, t 2.61, 515 cases). The flattest fifth gets −0.53 % (t −1.39).
- **F2:** The net 30-day move as a share of the 30-day closing range predicts the 5-day return above drift with a positive slope (0.0077, t 2.26, 2555 non-overlapping cases). Its top fifth (net/range +0.84) gets +0.98 % (t 1.76), and the second-lowest fifth −1.18 % (t −2.83). This is continuation of the month's direction, not reversion.
- **F3:** The tested forecast's edge is confined to 2018–2021. Its yearly slopes are 0.029 to 0.055 there (t 1.29 to 2.79), and −0.007 to −0.013 in each of 2022–2025 (t −0.74 to −0.78). The net-move slope does the same: 2018–21 0.0154 (t 3.00, 1278 cases), 2022–25 −0.0012 (t −0.28, 1277 cases).
- **F4:** A large day relative to the coin's 20-day volatility is followed by a higher 5-day return above drift.
- **F5:** The book's gain is carried by long holdings, not by the forecast's level.
- **F6:** The book's gain sits in a few days. Its best 5 % of days sum to 2.73 times its total gain. On its best 2 % of days the book makes +5.1 % while the coins make +8.3 %. On its worst 2 % it loses −4.5 % against the coins' −9.5 %.
- **F7:** 5-day stretches starting Monday or Tuesday beat the other weekdays by 1.98 % above drift (Welch t 4.72, 973 vs 2446 cases), in both 2018–21 (+1.71 %, +1.12 %) and 2022–25 (+1.15 %, +1.71 %).

## Ideas
- `023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation.g1_monthly-trend-share-continuation` (from F1, F2, F3): The larger a coin's net 30-day move up relative to its 30-day closing range, the larger its rise over the next 5 days.
- `023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation.g2_volatility-scaled-day-momentum` (from F4, F3): The larger a coin's latest 1-day rise relative to its 20-day volatility of daily returns, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
