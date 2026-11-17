---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3458 USD
---
## Findings
- **F1:** Large volatility-scaled falls rebound only when the coin's 20-day volatility is high against its own 120-day average. In the top fall quartile, the next-day excess return is +0.0137 (t 3.75, n 342) in the highest volatility-ratio tercile, +0.0061 (t 2.50, n 369) in the middle tercile and -0.0017 (t -0.83, n 474) in the lowest. Ranking all falls by fall size × volatility ratio gives quintiles 0–2 near zero (-0.0004 to -0.0012), quintile 3 at +0.0026 (t 1.74) and quintile 4 at +0.0081 (t 4.34, n 948).
- **F2:** Large falls on heavy volume rebound and large falls on light volume do not, which is the opposite of the brief's low-volume reasoning. Among the two lowest z-deciles, the next-day excess return is +0.0065 (t 4.52, n 1597) when the day's volume is in the top tercile against its 20-day mean, and +0.0005 (t 0.22, n 493) in the bottom tercile. Ranking falls by fall size × volume ratio puts the whole effect in the top quintile: +0.0062 (t 3.44, n 948), with the other quintiles between -0.0001 and +0.0011.
- **F3:** The heavy-volume rebound lasts two days. Over non-overlapping 2-day samples, falls on top-tercile volume are followed by +0.0061 (t 2.20, n 788), against -0.0032 (t -1.40, n 740) on bottom-tercile volume.
- **F4:** The two conditions add up. Top-quartile falls with high volume in a high-volatility regime return +0.0159 the next day (t 3.33, n 229). The same high-volume falls in a low-volatility regime return -0.0029 (t -1.02, n 281).
- **F5:** The rebound does not cluster around the return of weekday trading, so it gives no support to the weekend mechanism. Big falls on Monday bars are followed by -0.0006 (t -0.27, n 557), while Tuesday to Thursday falls give +0.0061 to +0.0066 (t 2.3–2.9). The book's mean daily gain on Monday is 0.000034 (t 0.10).
- **F6:** The rebound depends heavily on the period. Big falls give +0.0139 (t 4.00) in 2020 and +0.0137 (t 3.97) in 2021. In 2019, 2022, 2024 and 2025 they give -0.0014 to +0.0005, with |t| < 0.7.

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds.g1_falls-rebound-in-turbulence` (from F1, F4, F6): After a coin's daily fall, the coin rises over the next 1 day, and the rise is larger the larger the fall in units of its 20-day volatility multiplied by how high that 20-day volatility stands against its own 120-day average.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds.g2_heavy-volume-falls-rebound` (from F2, F3, F4): After a coin's daily fall, the coin rises over the next 2 days, and the rise is larger the larger the fall in units of its 20-day volatility multiplied by that day's volume relative to its 20-day average volume.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
