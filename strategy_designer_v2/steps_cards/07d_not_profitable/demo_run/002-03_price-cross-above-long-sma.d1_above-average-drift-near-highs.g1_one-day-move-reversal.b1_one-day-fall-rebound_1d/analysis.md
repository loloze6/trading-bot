---
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5230 USD
---
## Findings
- **F1:** The gain comes almost entirely from bars where the price stands far from its 50-day average, measured in units of 60-day volatility: the far tercile nets 0.003345 per active bar and carries 61% of the book's net gain, the mid tercile nets -0.000387, and the near tercile nets 0.000641; by sixths of that distance, the top two net 0.004701 (t 4.59, n 946) and 0.001989 (t 2.25, n 946), while the lower four lie between t -1.07 and t 1.11.
- **F2:** Inside the far tercile, the forecast's gradient holds. The next-day return falls as the one-day fall shrinks: 0.0102 for the largest falls (t 3.83, n 483), then 0.0113 (t 4.65), 0.0081 (t 2.61), 0.0048 (t 1.56) and 0.0025 (t 0.93) for the smallest. In the mid tercile even the largest falls are followed by only 0.00085 (t 0.31, n 347), with -0.001183 net.
- **F3:** Trading only the far tercile lifts Calmar from 0.43 to 1.00, cuts the deepest fall from -30.7% to -11.7% and lifts Sharpe from 0.585 to 0.90. Its mean daily return drops to 0.000327, but weighting by distance raises the mean to 0.000764 (Calmar 0.746), and leaving out only the mid tercile gives a mean of 0.000520 and Calmar 0.72.
- **F4:** The book's deepest fall, -30.7% over 120 days from w8 into w9, came while the coins fell 40.2%. In w9 the mid-distance bars below the average lost -0.595 in summed net (68 bars, next-day mean -0.0085), while the far-below bars earned +0.595 (109 bars, next-day mean +0.0079).
- **F5:** Far-tercile bars lose over a whole window in only 12.5% of the 24 windows, against 50% for near bars and 54% for mid bars.
- **F6:** Small falls do not pay their fees: the two smallest fall quintiles net -0.000127 and -0.000030 on fees of 0.000258 and 0.000193. The largest-fall quintile nets 0.003957 and carries 54% of the net gain.
- **F7:** The far-tercile rebound holds on both sides of the average: the next-day return is 0.0058 above it (n 880) and 0.0092 below it (n 1012).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound.d1_fall-rebound-when-stretched` (from F1, F2, F3, F4, F5, F7): The larger a coin's one-day fall relative to the standard deviation of its daily returns over the past 20 days, the larger its rise over the next day, only while its close stands far from its 50-day average in units of its 60-day daily volatility, and the more so the farther it stands.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound.d2_stretch-weighted-dip-rebound` (from F1, F2, F3, F6): The farther a coin's close stands from its 50-day average in units of its 60-day daily volatility, the larger its rise over the next day after a one-day fall, in proportion to the fall's size relative to its 20-day standard deviation of daily returns.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
