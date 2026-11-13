---
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
idea tested: 002-04_price-cross-below-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.3334 USD
---
## Findings
- **F1:** Over the 930 non-overlapping 10-bar blocks with a short position, the mean excess short gain is +0.0007 per block against a block standard deviation of 0.140 (t = 0.16, hit rate 52.5%), so the effect is roughly 1/200 of the noise; the pooled main measure is -0.0007 (t = -0.27).
- **F2:** The coin's own 10-bar return while short correlates 0.82 with the equal-weight 10-bar return of the six coins, so market moves dominate. Removing the market cuts the standard deviation from 0.140 to 0.079 but leaves no edge: relative short gain is -0.0003, t = -0.10.
- **F3:** The sign of the effect flips by year. Short gains were positive in 2018 (+0.039, t = 2.32, n = 134), 2019 (+0.012, t = 1.37) and 2022 (+0.023, t = 2.48, n = 195). They were negative in 2020 (-0.043, t = -2.73, n = 88), 2021 (-0.051, t = -2.32, n = 74) and 2023–2025 (-0.008 to -0.015). Bear-market and rebound years cancel each other.
- **F4:** By window the spread is also wide and opposite-signed. w7 (+0.058, t = 3.35), w9 (+0.040, t = 3.71) and w2 (+0.042, t = 2.45) are positive. w23 (-0.067, t = -3.12), w21 (-0.036, t = -2.75) and w16 (-0.042, t = -2.11) are negative.
- **F5:** No coin carries the effect. Per-coin mean short gains range from -0.004 (LTC, t = -0.39) to +0.006 (BTC, t = 0.59), all with |t| < 0.6.
- **F6:** Deeper forecasts are not better and the response is not monotonic. The deepest forecast quintile (mean -16.7) loses -0.013 (t = -1.14), while the second quintile (mean -10.6) gains +0.013 (t = 1.53). The deepest raw-distance quintile (-45% below the SMA) gains -0.001 (t = -0.10). This matches the negative supporting slope of -0.0056.
- **F7:** The effect leans toward long stays below the average. Blocks 61–150 days into a run below the SMA200 gain +0.017 (t = 1.81, hit 55%, n = 210), against -0.004 (t = -0.37, n = 283) in the first 20 days and -0.002 (t = -0.32) at 21–60 days. The 61–150-day gain stays positive net of the market (+0.006, t = 1.49).
- **F8:** Blocks where the SMA200 itself fell most over the prior 20 bars (quartile 0, mean slope -8.9%) gain +0.018 (t = 1.83, n = 199), against -0.002 to +0.001 in the other quartiles. This gain is pure market move: relative to the market it is +0.0002, t = 0.05.
- **F9:** Shorts taken after the steepest prior 30-day falls (bottom quartile, mean -27.5%) lose -0.009 (t = -0.89). Those after moderate falls (mean -10%) gain +0.014 (t = 1.90). Shorting after the sharpest drops runs into rebounds.
- **F10:** How many of the six coins sit below their average at the same time does not sort results once the market is removed. Relative short gain ranges from -0.005 to +0.001 across breadth groups, all with |t| < 1.1, including the 364 blocks when all coins were below.

## Ideas
- `002-04_price-cross-below-long-sma.b1_long-stay-below-average` (from F7, F1): When a coin's close has stayed below its 200-day SMA for roughly two to five months without interruption, the coin keeps falling over the next 10 days, by more than its usual drift and more than the six-coin market.
- `002-04_price-cross-below-long-sma.b2_steeply-falling-long-average` (from F8, F3, F2): When a coin's close is below its 200-day SMA and the SMA200 itself has fallen steeply over the prior 20 bars, the coin falls further over the next 10 days than its usual drift.
- `002-04_price-cross-below-long-sma.b3_moderate-decline-below-average` (from F9, F6): When a coin's close is below its 200-day SMA after a moderate decline over the prior 30 days (around 10%, not a crash), the coin keeps falling over the next 10 days, by more than its usual drift.
- `002-04_price-cross-below-long-sma.b4_moderate-depth-not-extreme` (from F6, F9): When a coin's close sits moderately below its 200-day SMA (the second-deepest fifth of the standardised distance, not the deepest), the coin falls further over the next 10 days than its usual drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
