---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3428 USD
---
## Findings
- **F1:** The tested idea's edge is a rebound after heavy-volume falling days, not after volume surges in general. In the top fifth of the volume ratio (today's volume over its prior 20-day mean), next-day excess return is +1.074 % (t 5.19, n 923) when the day's return is in the coin's bottom fifth. When that day's return is in the top fifth, it is −0.152 % (t −0.81, n 957).
- **F2:** Close location in the day's range adds to this. In the top volume fifth, next-day excess return is +1.061 % (t 5.60, n 897) when the close sits in the lowest third of the range. It is +0.148 % (t 0.76, n 884) in the middle third and −0.068 % (t −0.39, n 1129) in the top third. In no other volume fifth does the low-close third exceed |t| 1.3.
- **F3:** Volume is what makes a falling day rebound. Across all days, bottom-fifth return days are followed by +0.456 % (t 4.64, n 3438). On low-volume days (bottom two volume fifths) the same falling days are followed by only +0.011 % (t 0.06, n 687).
- **F4:** The rebound is several times the cost of a trade, unlike the tested idea's average case. The rebound of +1.06 % per day is about 5.6 times the 0.19 % cost. The tested idea's total move of +0.21 % is 1.1 times the cost.
- **F5:** Falling days carry most of the book's gain. Its in-position gain on bars whose day return is in the bottom fifth sums to 8.49 out of about 13.16 in total (65 %), at +0.452 % per bar (n 1880). Top-fifth return days give +0.101 % per bar (n 1972).
- **F6:** The heavy-volume effect is strongest when the coin is already volatile. In the highest third of 20-day volatility, the top volume fifth is followed by +0.838 % (t 3.27, n 913). In the middle third it is −0.013 % (t −0.08, n 965), and in the lowest third +0.245 % (t 1.97, n 1032).
- **F7:** The effect is uneven across years and coins. Heavy-volume days (top two fifths) are followed by +0.922 % (t 3.61) in 2021, +0.402 % in 2020 and +0.355 % in 2024. In 2018 the figure is −0.327 % and in 2019 −0.205 %. Every coin's top volume fifth is positive (+0.22 % to +0.66 %), but only ZEC's has t above 2 (2.23).

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound` (from F1, F3, F4, F5, F6): The more a coin falls on a day whose volume is heavy against its own prior 20-day average, the more it rises over the next day. The rebound grows both with the size of the day's fall and with how heavy the volume was, and it is largest when the coin's 20-day volatility is high.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal` (from F2, F1, F4): On a day whose volume is heavy against the coin's prior 20-day average, the lower the close sits within that day's high-low range, the more the coin rises over the next day. The heavier the volume, the stronger the link.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
