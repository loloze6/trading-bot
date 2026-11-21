---
line: 7.g patterns
backtest: 022-03_combined-extremes-larger-moves_1d
idea tested: 022-03_combined-extremes-larger-moves
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5739 USD
---
## Findings
- **F1:** The larger a coin's last 1-day move relative to its 30-day daily volatility, in either direction, the higher its unusual return over the next 5 days. Rank correlation is 0.057 (t 3.06, 2843 non-overlapping 5-day cases), and it is positive in all 6 coins (0.031 to 0.096). The top fifth of moves is followed by an unusual move of +1.02 % (strength 0.092, t 2.32, 571 cases) and a total move of +1.71 %. That is about 5 and 9 times the 0.19 % cost of a buy and a sell.
- **F2:** This follow-through comes mostly after large up days. The rank correlation of move size with the next 5-day unusual return is 0.069 (t 2.53, 1355 cases) after up days and 0.046 (t 1.79, 1488 cases) after down days. The two largest fifths of up days are followed by unusual moves of +1.40 % (t 2.01, 259 cases) and +1.59 % (t 2.23, 293 cases), with total moves of +2.09 % and +2.29 %. The largest fifth of down days is followed by +0.42 % (t 0.92).
- **F3:** The large-move effect is stronger in later years (rank correlation 0.076, t 2.95, 1493 cases for 2022 to 2025) than in earlier ones (0.038, t 1.39, 1350 cases for 2018 to 2021). By year it is positive in 7 of 8 years, highest in 2021 (0.156) and 2024 (0.165).
- **F4:** The tested combined score points the wrong way, but too weakly to trade the other way. Its rank correlation with the next 5-day unusual return is -0.036 (t -2.03, 3254 cells), negative in 7 of 8 years and 5 of 6 coins. Inverting its top 10 % gives only +0.05 of a usual move (t 0.80, 326 cases).
- **F5:** The book loses through its timing, not through the market's drift. Its position's gain per bar is negative in 5 of 6 coins (-1.8 to -8.7 bps per bar), while the part from the market's own rise is only -0.1 to -1.3 bps per bar.
- **F6:** Daily returns differ by weekday.

## Ideas
- `022-03_combined-extremes-larger-moves.g1_large-up-days-keep-rising` (from F1, F2, F3): The larger a coin's 1-day rise relative to its daily volatility over the past 30 days, the more the coin rises above its normal drift over the next 5 days.
- `022-03_combined-extremes-larger-moves.g2_violent-days-precede-gains` (from F1, F3): The larger a coin's 1-day move in either direction relative to its daily volatility over the past 30 days, the higher the coin's return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
