---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day_1h
idea tested: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4481 USD
---
## Findings
- **F1:** A coin's 24-hour fall reverses over the next 24 hours only when its volatility is high. In the top tercile of each coin's 30-day hourly volatility, the 24h-return quintiles (24h return scaled by its usual 24h move) give an excess return over the next 24h of +1.25 % (t 5.12, 1012 cases) for the largest falls and −0.69 % (t −3.14, 991 cases) for the largest rises. In the low-volatility tercile the same quintiles give +0.02 % (t 0.14) and +0.17 % (t 1.49).
- **F2:** The reversal grows with volatility measured against the coin's own past. Sorting the 24h grid cases by 30-day volatility over its 90-day median, the slope of the next-24h excess return on the scaled 24h return is +0.3 bp (t 0.06), −14.0 bp (t −2.80) and −33.2 bp (t −6.65) from the low to the high tercile (about 4309 cases each).
- **F3:** In high volatility the reversal is graded. Across the fall quintiles, the next-24h excess return climbs from −0.38 % (t −1.45) for the mildest falls to +1.64 % (t 4.16, 424 cases) for the largest. +1.64 % is 8.6 times the 0.19 % cost of a trade, against the tested idea's total move of +0.23 % per case.
- **F4:** The high-volatility 24h reversal holds coin by coin and year by year, with differing strength:
- **F5:** The 2-hour move reverses over the next 24h most strongly on bars closing at 00:00, 01:00 and 02:00 UTC (t −6.32, −8.53, −7.83, about 15,900 bars each).
- **F6:** At the 00:00–02:00 UTC closes, the 2-hour move keeps its reversal when the 24h move is in the same regression: coefficients −13.5 bp (t −8.96) for the 2h move and −15.5 bp (t −9.63) for the 24h move. It is negative in all six coins (t −3.52 to −8.13) and in seven of eight years (2022: +0.7 bp, t 0.20).
- **F7:** The bar after a close at 21:00 or 22:00 UTC rises on average +5.09 bp (t 6.01) and +4.60 bp (t 5.73). This holds in seven of eight years (2022: −2.18 bp, t −1.44). The roughly 10 bp over the two hours is about half the 0.19 % cost of a trade, so it is not tradable on its own.

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.g1_high-volatility-daily-move-reverses` (from F1, F2, F3, F4): When a coin's hourly volatility over the past 30 days is high against its own past 90 days, its return over the next 24 hours runs opposite to its 24-hour return. The larger the 24-hour move against its usual 24-hour move, and the higher that relative volatility, the larger the reversal.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.g2_early-utc-two-hour-fall-recovers` (from F5, F6): A coin that falls over the 2 hours ending at 00:00, 01:00 or 02:00 UTC rises over the following 24 hours, more strongly the larger that fall against its usual 2-hour move. The rise comes on top of the reversal of its 24-hour fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
