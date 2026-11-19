---
line: 7.g patterns
backtest: 016-01_up-grind-price-continuation_1h
idea tested: 016-01_up-grind-price-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3316 USD
---
## Findings
- **F1:** The size of a coin's 3-day move, in either direction, carries the next 3 days' rise. On the non-overlapping 72-bar grid, the largest third of 3-day moves was followed by a mean next-72-bar return of +0.0124 after rises (t 3.82, n 978) and +0.0090 after falls (t 2.82, n 869). The smallest third gave +0.0005 after small rises (t 0.19) and -0.0046 after small falls (t -1.92). In a pooled regression on standardised values, the 3-day move's absolute size has a beta of 0.0050 (t 4.38) and its signed value a beta of -0.0067 (t -2.73).
- **F2:** UTC hours 20 and 21 carry a large share of the coins' rise. Their mean hourly returns are +0.000545 (t 6.75) and +0.000436 (t 5.66), against a range of -0.000356 to +0.000271 for the other 22 hours. The excess of hours 20-21 over the other hours is positive in all 6 coins (+0.00041 to +0.00053, Welch t 2.66 to 4.10) and in 7 of 8 years (Welch t 1.43 to 4.95 in those 7; 2022 is -0.00017, t -1.07).
- **F3:** The tested grind share mostly measures the move's size, and the book lost money. Across up-move terciles of the share, the next-72-bar return rises from -0.0010 to +0.0039 to +0.0126, but the past 3-day rise grows with it, from 0.015 to 0.053 to 0.112. At the forecast's own split the top-minus-bottom difference is -0.0043 (Welch t -0.57, 316 cases per third). The book's mean daily return was -0.000522, against +0.00119 for holding the coins.
- **F4:** Signed path efficiency (net 3-day log move over the sum of absolute hourly log moves) has a top quintile with a next-72-bar mean of +0.0108 (t 3.98, n 1108), and it keeps a beta of 0.0081 (t 3.36) beside size and direction. It is not stable, though. The top-minus-bottom difference reaches t 2 in no coin (-0.12 to 1.77), and by year it flips sign: +0.033 (t 2.81) in 2018 and -0.026 (t -2.18) in 2021. I do not count it as a pattern apart from chance.
- **F5:** Weekdays differ too: Friday's mean hourly return is +0.000264 (t 5.83) and Thursday's is -0.000146 (t -3.22). I did not check this by coin or by year, so it does not stand on its own.

## Ideas
- `016-01_up-grind-price-continuation.g1_big-moves-precede-rises` (from F1, F3): The larger a coin's absolute 3-day return, whether up or down, the more the coin rises over the next 3 days.
- `016-01_up-grind-price-continuation.g2_persistent-hour-of-day-drift` (from F2): The higher a coin's average return in a given UTC hour of day over its past 30 days, the more the coin rises during that same hour over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
