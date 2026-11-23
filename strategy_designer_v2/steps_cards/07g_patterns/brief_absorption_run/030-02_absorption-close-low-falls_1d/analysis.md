---
line: 7.g patterns
backtest: 030-02_absorption-close-low-falls_1d
idea tested: 030-02_absorption-close-low-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5424 USD
---
## Findings
- **F1:** On days with volume above 1.5 times the prior 20-day mean, the next day's return above the coin's drift falls steadily as the close moves up the day's range: +1.57 % (t 5.18, 413 cases) when the close is in the lowest fifth, +0.28 %, +0.19 % and +0.22 % in the three middle fifths, and −0.19 % (t −0.82, 590 cases) in the top fifth. The low-close next-day rise, +1.70 % before removing drift, is about 9 times the 0.19 % cost of a trade.
- **F2:** The close location only predicts the next day when volume is heavy. In a regression on (0.5 − close location) that controls for the day's return over its 20-day volatility, the close-location slope is 0.0238 (t 2.65, n 1292) when volume is above 2 times its mean, 0.0143 (t 2.34, n 2515) above 1.5 times, and 0.0001 (t 0.02, n 8994) below 1 time. Over all days the close-location × volume-ratio interaction has t 6.00 (n 14500).
- **F3:** On days with volume above 1.5 times its mean, the next-day excess of low-close days minus high-close days is positive in 7 of 8 years. It ranges from +0.41 % to +4.04 % and has t above 2.2 in 2018, 2019, 2020 and 2025; the only negative year is 2021 (−0.11 %, t −0.10). The low-close slope is positive for all 6 coins, with t 2.4 to 2.8 for BTC, ETH, LTC and XMR and t 0.7 to 0.9 for XRP and ZEC.
- **F4:** The effect is a next-day reversal that fades within three days. Over all days, the slope of the excess return on low close has t 4.66 over 1 day (n 17379), t 1.92 over 2 days and t −0.91 over 3 days. At the tested idea's 5-day horizon, the flat heavy-volume days number only 23 non-overlapping cases with no pattern. The book lost on every coin, with mean net trade results of −1.8 % to −4.4 %.
- **F5:** Over all days, the more a coin fell on a day, the more it rose the next day. The lowest fifth of day returns was followed by +0.48 % above drift (t 4.88, 3448 cases) and the highest fifth by −0.23 % (t −2.40). The day's return over its 20-day volatility keeps t −4.66 next to the range-tail measures. This general reversal is about 0.5 % a day, only 2.5 times the cost of a trade.

## Ideas
- `030-02_absorption-close-low-falls.g1_heavy-volume-low-close-rebounds` (from F1, F2, F3, F4): On a day when a coin's volume is above its 20-day average, the closer its close sits to the day's low, the more the coin rises over the next 1 day, and the effect is larger the heavier that day's volume is against its 20-day average.
- `030-02_absorption-close-low-falls.g2_one-day-volatility-scaled-reversal` (from F5, F4): The more a coin's daily return falls below zero, measured against its 20-day volatility, the more the coin rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
