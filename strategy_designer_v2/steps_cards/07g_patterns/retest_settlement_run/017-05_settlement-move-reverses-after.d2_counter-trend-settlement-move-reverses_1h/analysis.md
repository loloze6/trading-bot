---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h
idea tested: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4387 USD
---
## Findings
- **F1:** Over the next 24 hours a coin reverses its own 24-hour return, and the reversal grows with the size of that return. Measured on the 24-bar grid, the reversal rises from -4.9 bp in the smallest |24h return| quintile to +13.4 bp in the fourth and +64.3 bp in the largest (t 5.1, 2585 cases). Read as a slope, it is +52.6 bp per usual 24h move of |24h return| (t 8.9, 12926 cases).
- **F2:** In the largest |24h return| quintile the reversal holds across the data. It is positive in every coin, from +50.9 bp in ETH to +86.5 bp in ZEC (t 1.5 to 3.2, about 435 cases each), and in 79 % of the 24 windows. Its strength is 0.13 of the coin's usual 24h move, well above the 0.05 typical of real ideas. Its total move of +63.6 bp is 3.3 times the 0.19 % cost of a trade.
- **F3:** The reversal is lopsided by side. After the largest 24h falls the next 24h excess return is +96.9 bp (t 5.1, 1240 cases), against +34.2 bp of reversal after the largest 24h rises (t 2.1, 1345 cases).
- **F4:** The 24h reversal is concentrated where 24h volatility is high against its 30-day level. It is +56.3 bp in the top quintile of vol24/vol720 (t 4.7, 2585 cases), against -14.8 to +15.6 bp in the other four (|t| below 1.8).
- **F5:** The 2-hour move also reverses over the next 8 hours, graded by its size: from -1.3 bp in the smallest |2h| quintile to +6.4 bp (t 2.4) in the fourth and +15.7 bp (t 4.1, 10369 cases) in the largest. This total move is below the 0.19 % cost of a trade.
- **F6:** The 8h reversal of the 2h move is not tied to funding times. At the 08:00 settlement it is -2.8 bp (t -1.2), while at 04:00, a time with no funding, it is +4.5 bp (t 2.2), next to +12.2 bp at 00:00 (t 6.1) and +7.3 bp at 16:00 (t 3.3; about 17300 cases each). The idea's own measure has a strength of 0.007 and a mean of only +0.02 % per case (t 1.25).
- **F7:** The book lost through its shorts. Short trades averaged -0.41 % before fees against +0.23 % for longs (about 16000 trades each side). The book's daily mean was negative every year from 2022 to 2025 (-8.5 to -11.9 bp, t -2.6 to -3.8), for a Sharpe of -0.83.
- **F8:** The 1-hour excess return has a clock pattern unrelated to settlement. It is high on bars closing at 21:00 and 22:00 UTC (+4.8 bp t 6.0, +3.7 bp t 4.8) and low on bars closing at 14:00 and 03:00 (-4.2 bp t -4.5, -3.4 bp t -4.6). Volume is highest from 15:00 to 17:00 (median 1.47 to 1.52 of the weekly median), not at the settlement hours.

## Ideas
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.g1_large-daily-move-reverses` (from F1, F2, F7): The larger a coin's 24-hour return relative to its usual 24-hour move, the more strongly its price moves the opposite way over the next 24 hours.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.g2_sharp-daily-fall-rebounds` (from F3, F1, F7): The deeper a coin's 24-hour fall relative to its usual 24-hour move, the larger its rise over the next 24 hours.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.g3_volatility-burst-move-reverses` (from F4, F1): When a coin's 24-hour volatility is high against its 30-day volatility, its 24-hour return reverses over the next 24 hours, and the higher that ratio, the larger the reversal.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.g4_sharp-two-hour-move-reverses` (from F5, F6): The larger a coin's 2-hour return relative to its usual 2-hour move, the more its price moves the opposite way over the next 8 hours, at any time of day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
