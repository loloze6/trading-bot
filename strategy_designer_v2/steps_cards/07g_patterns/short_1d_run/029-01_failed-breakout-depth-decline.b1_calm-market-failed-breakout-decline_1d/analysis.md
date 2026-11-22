---
line: 7.g patterns
backtest: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d
idea tested: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3894 USD
---
## Findings
- **F1:** The tested situation shows no fall. On a 5-day grid, the 245 failed-breakout cells were followed by a 5-day return +0.263 % above the coin's mean (t 0.36), against −0.020 % (t −0.10, 3174 cells) for all other cells. The step-5 cases gave −0.11 % per case in the short direction (t −0.27, 615 cases). The book earned less than holding in every coin, from +0.0016 % to −0.048 % a day, while active on 15 % to 26 % of days.
- **F2:** A large up day was followed by a further rise. Cells in the top quintile of the day's return divided by its 20-day volatility gained +1.63 % above the coin's mean over the next 5 days (t 3.24, 570 cases), the only quintile clearly away from zero. The bottom quintile was −0.28 % (t −0.73).
- **F3:** The rise after a large up day is graded and widespread. The 5-day excess return in volatility units rises with the day's return in all six coins, significantly in XMR (t 2.12), XRP (t 2.86) and ZEC (t 2.51). Top-quintile cells were positive in 5 of 6 coins (BTC +1.61 % t 1.94, ZEC +3.91 % t 2.09; LTC −0.21 % the exception) and in 6 of 8 years (2021 +5.15 % t 3.19, 2024 +2.47 % t 2.06; 2022 −0.90 % t −0.93).
- **F4:** A close above the prior 20-day high was followed by +1.62 % over 5 days (t 2.18, 306 cases), but this rests on XRP (+10.2 %, t 2.40) and on 2020–2021 (+5.3 %, +8.4 %). It reversed in 2022 (−3.58 %, t −2.42), so it is not a stable pattern on its own.
- **F5:** A large down day was followed by a one-day rebound. Days in the bottom quintile of the day's return divided by its 20-day volatility were followed by a next-day return +0.39 % above the coin's mean (t 4.07, 2903 days). The other quintiles ran from +0.05 % to −0.23 %.
- **F6:** The one-day rebound is positive in all six coins (XMR +0.83 % t 3.95, the others +0.14 % to +0.43 % with t 0.8 to 1.5). It is concentrated in 2020 (+1.22 %, t 3.47), 2021 (+1.21 %, t 3.76) and 2023 (+0.37 %, t 2.22), and near zero in 2024–2025 (−0.02 %, −0.10 %). Its +0.39 % barely exceeds the 0.19 % cost of a trade.
- **F7:** Weekday effects exist over one day but are not graded situations. Fridays were followed by +0.31 % (t 3.76), positive in 5 of 6 coins and in 6 of 8 years. Mondays and Wednesdays were followed by −0.24 % (t −2.53) and −0.30 % (t −2.70).

## Ideas
- `029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline.g1_strong-up-day-continues` (from F1, F2, F3): The larger a coin's daily return measured in units of its 20-day volatility of daily returns, the more the coin rises over the next 5 days.
- `029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline.g2_large-down-day-rebounds` (from F5, F6): The larger a coin's daily fall measured in units of its 20-day volatility of daily returns, the more the coin rebounds over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
