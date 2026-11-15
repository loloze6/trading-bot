---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3248 USD
---
## Findings
- **F1:** The edge is too small to separate from noise at the plan's horizon. On the 399 non-overlapping 20-day cases above the 200-day SMA, the mean excess return over holding is 0.0052 (t 0.32), against -0.0002 on the 412 cases below it (Welch t 0.27).
- **F2:** The positive mean comes from a few large gains, not from most cases. Above the SMA, the median 20-day excess is negative and the share beating holding is under 50% at every horizon: 46.9% at 5 days (n 1640), 44.9% at 10, 40.6% at 20, 37.7% at 40 (n 191) and 38.3% at 60 (n 120).
- **F3:** Only the strongest forecasts show a gain, and even there the typical case loses. The top forecast quartile (mean forecast 19.3, n 100) has a mean 20-day excess of +0.072, but its median is -0.015 and only 42% of its cases beat holding. Quartiles 1 to 3 (forecasts 2.1 to 12.6) all have negative means (-0.035, -0.004, -0.013).
- **F4:** There is no grading by raw distance from the SMA. Across six sextiles running from -41% to +79%, the 20-day excess means are 0.001, 0.019, -0.016, -0.015, 0.012 and 0.013, and the two highest sextiles beat holding only 34.8% and 41.2% of the time.
- **F5:** The effect changes sign between coins and between periods.
- **F6:** Sizing by volatility is what lifts the measure. The plan's allocation-weighted main measure reaches t 1.73. The same cases with equal weights give only t 0.32. The allocation is volatility-targeted on 60-day volatility, so the effect leans toward the calmer stretches, where positions are larger.
- **F7:** The book earns more from the market's own rise than from timing. Its mean daily return is 0.000554, of which 0.000345 is the market's rise at a mean allocation of 0.27, and only 0.000209 is timing.

## Ideas
- `002-03_price-cross-above-long-sma.b1_above-sma-trend-in-calm-regimes` (from F6, F1, F5): While a coin's close is above its 200-day simple moving average, the further above it sits relative to its own past distances, the more the coin outperforms its average return over the next 20 days, only while its 60-day volatility is low relative to its own past.
- `002-03_price-cross-above-long-sma.b2_extreme-distance-above-sma` (from F3, F2, F4): While a coin's close is above its 200-day simple moving average, the further above it sits relative to its own past 200 days of distances, the larger the coin's gain over its average return over the next 20 days, with the gain concentrated in the most extreme distances.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
