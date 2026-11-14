---
line: 7.g patterns
backtest: N4-01_breakout-drift-lasts_1d
idea tested: N4-01_breakout-drift-lasts
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2996 USD
---
## Findings
- **F1:** A daily close down more than 0.5 of its 20-day volatility is followed by a rise the next day. In the (-1.5,-0.5] band the mean is +0.46% (t 4.82, n 2796, hit 56%); in the (-2.5,-1.5] band it is +0.49% (t 2.38, n 662, hit 61%). Days with no move average 0.01% (t 0.13, n 6729), and up moves above +0.5 sd average about 0% (hit 42–46%).
- **F2:** The down-day rebound holds in all six coins, at +0.29% to +0.83% next day (t 1.64 to 4.68, hit 55–61%, n 577–653 each). It is positive in every year, from +0.11% to +1.20%, and is significant in 2018, 2020, 2021 and 2023. Over non-overlapping 3-day spans, down days are followed by +0.93% (t 3.39, n 1172) against +0.21% (t 1.76, n 4551) for other days.
- **F3:** Where the close sits in the day's range predicts the next day in order. Closes in the bottom fifth of the range are followed by +0.50% (t 5.03, n 2655, hit 57.7%), and closes in the top fifth by -0.10% (t -1.21, n 3735, hit 44.8%). Among down days, those closing in the bottom third rebound +0.55% (t 5.71, n 2675). The 56 down days that closed in the top third show no rebound (-0.83%, t -1.15).
- **F4:** Returns after Thursday and Friday UTC closes are positive: +0.37% (t 3.89, n 2483) and +0.42% (t 5.23, n 2479). Returns after Monday and Wednesday closes are -0.12% and -0.18%. The Thursday/Friday effect is positive in all six coins (t 1.87–3.76) and in 7 of 8 years (t above 2 in 2019, 2020, 2023, 2024 and 2025). The book makes most of its money on those same days: +0.45% (t 3.90) and +0.47% (t 4.79) per day.
- **F5:** The 10-day drift after a high is concentrated at the exact 20-day closing high. Non-overlapping 10-day returns from closes at the top of the range average +5.3% (t 3.25, n 179); every lower fifth of the range gives +0.2% to +1.3% (t below 1.9). Among new highs, those above their 50-day average give +6.1% (t 2.90, n 113, hit 58%); those below it give +3.7% (t 1.24, n 57, hit 42%).
- **F6:** The book's losing trades are the short ones. Trades of 15 days or less lose on average: -9.2%, -4.7%, -4.5% and -3.4% by duration band, with win rates of 2–32% over 1563 trades. Trades longer than 15 days earn +11.9% (median +3.1%, win rate 55%, n 1705). The book is profitable only because some trades keep running long after the high.

## Ideas
- `N4-01_breakout-drift-lasts.g1_weak-close-next-day-rebound` (from F1, F2, F3): In each coin, a daily close that falls more than half a typical daily move and finishes in the lower part of the day's range is followed by a rise over the next one to three days.
- `N4-01_breakout-drift-lasts.g2_late-week-crypto-drift` (from F4): In each coin, the daily returns following Thursday and Friday UTC closes are higher than those following other weekdays' closes.
- `N4-01_breakout-drift-lasts.g3_uptrend-fresh-high-continuation` (from F5, F6): In each coin, a close at the exact 20-day closing high, made while price is above its 50-day average, is followed by a larger rise over the next ten days than closes elsewhere in the 20-day range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
