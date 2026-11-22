---
line: 7.b inconclusive
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h
idea tested: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3908 USD
---
## Findings
- **F1:** The tested idea's result is zero, not merely short of the bar. The mean unusual 18-bar move per case is -0.02 % (t -0.25, 12162 cases). No other horizon shows it either: 3 bars +0.02 % (t 0.67), 6 bars +0.09 % (t 1.02), 12 bars -0.01 % (t -0.17), 36 bars -0.05 % (t -0.36). Every coin's t lies between -0.70 and +0.49. The test already used all 19 coins and all four folds, so there is no more data to add.
- **F2:** The zero is two opposite effects that cancel, split by the coin's 30-day return at the signal bar. When the 30-day return is positive, the up-streak is followed by a further rise above drift: +0.26 % per case (t 1.76, 4545 cases), positive in 79 % of the coins. When it is negative, the streak is followed by a give-back: -0.46 % (t -3.64, 4557 cases).
- **F3:** Inside the 30-day up-trend, the effect grows with the streak's size, as the idea says. The top quartile of forecast (mean 19.3) gains +0.77 % (t 1.99, 1136 cases), against +0.21 % for the bottom quartile (mean 3.5). Inside the down-trend, the largest streaks are near zero (-0.22 %, t -0.82) and the smallest give back most (-0.67 %, t -2.69).
- **F4:** The 30-day return grades the result fairly steadily across its deciles. Deciles 1 to 5 (30-day returns from -23 % to +3 %) give unusual moves between -0.30 % and -1.19 %, with t down to -4.47. Deciles 6 to 9 (+9 % to +87 %) give between +0.25 % and +0.73 %. Only the deepest-fall decile (-37 %) breaks the pattern, at +0.99 % (t 2.88), which looks like a capitulation bounce. The 10-day return shows the same shape.
- **F5:** The up-trend continuation depends on the regime year to year. It is strong in 2020 (+0.97 %, t 2.48), 2021 (+2.66 %, t 3.97) and 2023 (+0.63 %, t 2.60), and reverses in 2018 (-4.82 %, t -5.73), 2022 (-1.41 %, t -3.62) and 2025 (-0.96 %, t -2.32). The down-trend give-back is negative in 7 of 8 years.
- **F6:** The brief's own condition, fading volume, does not separate the cases. Across quintiles of the last bar's volume against the streak's earlier bars, the unusual move ranges from -0.53 % to +0.23 %, with no t beyond ±1.35 and no order.

## Ideas
- `024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins.b1_up-streak-continuation-in-uptrend` (from F2, F3, F4, F5): When a coin has just risen in an unbroken streak of four-hour periods, it keeps rising over the next three days, only while its 30-day return is positive; the larger the streak's gain relative to the coin's typical four-hour move over the past 30 days, the larger the further rise.
- `024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins.b2_up-streak-giveback-in-downtrend` (from F2, F4): When a coin has just risen in an unbroken streak of four-hour periods while its 30-day return is negative, it gives back part of the streak over the next three days; the deeper the 30-day fall, the larger the give-back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
