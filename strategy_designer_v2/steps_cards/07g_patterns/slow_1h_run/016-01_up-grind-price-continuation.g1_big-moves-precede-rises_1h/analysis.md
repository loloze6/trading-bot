---
line: 7.g patterns
backtest: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h
idea tested: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3635 USD
---
## Findings
- **F1:** The coin rises more after its smoothest up moves: over all six coins and every window there were 5,539 non-overlapping 3-day cases. Among 3-day up moves, those in the top quintile of path efficiency (net 72-hour move divided by the sum of absolute hourly moves) were followed by a 72-hour excess return of +1.23% (t=3.26, n=638). The bottom quintile was followed by -0.45% (t=-1.21). The slope of the excess return on efficiency is 0.0565 (t=3.32, n=2,865) for up moves, against 0.0176 (t=1.00, n=2,674) for down moves.
- **F2:** Efficiency does not add to the move's size and volatility. When it shares a regression with the signed standardised 3-day move and the hourly volatility, efficiency's coefficient falls to -0.0022 (t=-0.04). The signed move keeps t=1.89 and volatility t=2.38. So the grind effect in F1 overlaps with plain 3-day momentum, which is positive in all six coins (slopes t 0.06 to 1.48).
- **F3:** The tested forecast's payoff is U-shaped in the signed 3-day move, not rising with its size. The excess 72-hour return is +0.29% (t=1.05) in the lowest quintile, -0.77% (t=-3.55) in the middle quintile and +0.67% (t=2.27) in the highest. This explains why the slope t of 3.67 came with negative timing in the book: timing part -0.0005 per day, Sharpe -0.38.
- **F4:** The straightness of the last 24 hours, in either direction, is followed by a higher return over the next 24 hours: slope 0.0176, t=3.92, n=5,539. It is also followed by a higher return over the next 72 hours: slope 0.0231, t=3.06.
- **F5:** The hour that follows the 20:00 and 21:00 UTC bars is the strongest of the day. The mean next-hour return is +0.055% (t=6.75) and +0.044% (t=5.66). Hours 20 and 21 together beat the other hours in all six coins (Welch t 2.66 to 4.10) and in 6 of 8 years (t 2.93 to 4.95). The exception is 2022 (t=-1.07).
- **F6:** Friday's hourly returns are higher overall (t=5.83), but the edge is concentrated in 2018 (t=4.04), 2019 (t=5.65) and 2023 (t=2.62). It is near zero in 2021, 2022, 2024 and 2025 (|t|<0.5). So it is too uneven across years to count as a stable pattern.

## Ideas
- `016-01_up-grind-price-continuation.g1_big-moves-precede-rises.g1_smooth-rises-keep-rising` (from F1, F2, F3): The more of a coin's 3-day rise is made of hourly steps in the same direction (its net 3-day move over the sum of its absolute hourly moves), the more the coin rises over the next 3 days.
- `016-01_up-grind-price-continuation.g1_big-moves-precede-rises.g2_straight-days-precede-rises` (from F4): The straighter a coin's last 24 hours (its net 24-hour move over the sum of its absolute hourly moves), the more the coin rises over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
