---
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
idea tested: 002-04_price-cross-below-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3041 USD
---
## Findings
- **F1:** The short gain beyond holding is close to zero at every horizon while the close is below the 200-day SMA (non-overlapping blocks: 1 day t -0.10 on 8674 cases, 5 days t -0.39 on 1709, 10 days t -0.70 on 841, 20 days t -0.01 on 412, 40 days t +0.26 on 197), so the test did not miss the effect by using the wrong horizon.
- **F2:** The effect is mixed across periods rather than small and uniform: the 10-day short excess gain is positive in 2018 (+0.040, t 2.41, n 137), 2019 (+0.016, t 1.87) and 2022 (+0.025, t 2.64, n 191), and negative in 2020 (-0.049, t -3.05, n 73), 2021 (-0.042, t -1.75), 2023 (-0.019) and 2024 (-0.015), so the years cancel each other in the pooled t of -0.23.
- **F3:** The years in which the short works are the sustained bear years. Consistent with that, the 10-day short excess gain is largest when the 200-day SMA itself has fallen most over the past 30 days: +0.0166 (t 1.74, n 205) in the steepest-falling tercile (mean SMA change -12 %), against +0.0035 (t 0.42) in the middle tercile and -0.0007 (t -0.07) where the SMA is rising.
- **F4:** Among bars below the SMA200, the 10-day short excess gain rises with the coin's own 60-day return, and this is the only significant result in the pooled data. It is -0.013 (t -1.00, n 135) after the largest 60-day falls (mean -39 %), +0.014 (t 1.42) in the middle tercile, and +0.027 (t 2.27, n 135) in the top tercile (mean +6 %, a rebound toward the falling average).
- **F5:** The top-60-day-return effect is positive in every coin, from ETH +0.008 to BTC +0.043 (t 0.25 to 1.39, 20 to 26 blocks each), so a few coins do not carry it.
- **F6:** The plan's grading by depth below the SMA does not hold. The deepest quintile of distance (mean -46 %) earns +0.0001 (t 0.00), and the shallow quintiles earn +0.007 to +0.011. The correlation of the short gain with distance is only 0.05, and the plan's regression slope is -0.013. Grading by depth adds the most size where the coin is already most sold-off, which is where it tends to bounce (F4).

## Ideas
- `002-04_price-cross-below-long-sma.b1_short-the-rebound-under-sma200` (from F4, F5, F6, F1): While a coin's close is below its 200-day simple moving average, it falls further than its usual drift over the next 10 days, and the more its 60-day return has recovered toward the average, the larger that fall.
- `002-04_price-cross-below-long-sma.b2_below-falling-sma200-persists` (from F2, F3, F1): While a coin's close is below its 200-day simple moving average, it falls further than its usual drift over the next 10 days, only while the 200-day average itself has been falling over the past 30 days, and the steeper that fall of the average, the larger the move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
