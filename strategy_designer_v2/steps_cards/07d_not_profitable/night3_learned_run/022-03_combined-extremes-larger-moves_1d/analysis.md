---
line: 7.d not profitable
backtest: 022-03_combined-extremes-larger-moves_1d
idea tested: 022-03_combined-extremes-larger-moves
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3998 USD
---
## Findings
- **F1:** The book's loss comes from its shorts. Summed over bars, short positions lost 10.22 against +2.98 for longs. The 2,281 short trades lost 5.58 % each after fees, while the 1,981 long trades gained 1.89 %. Of the book's -0.044 % mean gain per bar, -0.037 % is timing and only -0.007 % is the market's own rise.
- **F2:** The combined score is not just weak: its sign points the wrong way. On all 3,254 non-overlapping 5-day cells, the unusual move signed by the score averages -0.49 % (t -2.62), with a correlation of -0.035. On its top-10 % readings it averages -0.38 % (t -0.55, n 326). That is 0.1 times a round trip of 0.19 %, so no holding period or sizing can make the book pay.
- **F3:** The weights learned from the past do not carry forward, because each effect's sign flips from year to year. The Spearman correlation of 28-day momentum with the next 5-day move is -0.13 in 2018, +0.09 in 2021 and -0.13 in 2022. Nearness to the 90-day high goes from +0.16 in 2019 to -0.24 in 2022. Pooled over all years, every effect is near zero (|rho| ≤ 0.037, p ≥ 0.31).
- **F4:** The score's worst readings are its long ones while the coin's 90-day return is positive. There the signed 5-day unusual move is -2.05 % (t -2.83, n 172). In that trend state the book lost on both sides: -0.108 % per bar long (n 847) and -0.123 % per bar short (n 1,278).
- **F5:** Of the raw effects, only the strongest 28-day rises are followed by a move that clears the cost. The top coin-relative quintile of 28-day return has a next-5-day unusual move of +1.21 % (t 2.15, n 490), about 6 times a round trip. The other four quintiles lie between -0.73 % and +0.44 %, none with |t| above 1.8.
- **F6:** The book lost to holding in every year but 2018 and 2022. Its yearly Sharpe runs from -1.74 to +0.76. Over 2019–2025 it earned -0.03 % to -0.12 % a day, while holding earned +0.05 % to +0.42 %, the bull year 2022 aside.

## Ideas
- `022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue` (from F1, F3, F5): The larger a coin's 28-day rise relative to its own usual 28-day moves, the more the coin rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
