---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3361 USD
---
## Findings
- **F1:** Bar by bar the effect is close to zero. On the non-overlapping 20-bar grid, bars with forecast > 0 beat the coin's pooled mean by 0.0052 (t 0.32, n 399), against −0.00015 (t −0.01, n 412) for bars below the SMA. Only 40.6% of them win, and the median is −0.036. No horizon from 5 to 60 bars gets past |t| 0.61.
- **F2:** The plan's block t of 1.73 rests on a handful of blocks. The top 10 of 811 blocks sum to 132.7, more than the 102.4 total, while the bottom 10 sum to −41.5. Only 16–27% of each coin's blocks are positive. The effect therefore shows as rare large continuations, not frequent ones.
- **F3:** The effect splits by period. Forecast > 0 bars lost heavily in 2018 (−0.132, t −2.76, n 21) and 2022 (−0.173, t −3.12, n 10). They earned in 2020 (+0.022), 2024 (+0.021) and 2025 (+0.036), and 2020's blocks reached +0.46 (t 2.03). The above-SMA state reverses in bear years and persists in bull years.
- **F4:** Only the largest standardised forecasts carry a gain. The top forecast quartile gives +0.072 (t 1.34, n 100) and the bottom quartile −0.035 (t −1.81, n 100), with the middle two near zero (−0.004, −0.013). Raw-distance sextiles show no order (+0.0125 and +0.0128 for the two highest, −0.015 just above the SMA).
- **F5:** Prior momentum separates the cases. Among forecast > 0 bars, the lowest 20-bar momentum tercile gives −0.022 (t −1.13), the middle +0.025 (t 1.34) and the highest +0.042 (t 0.85), each n 110.
- **F6:** The gain grows with time spent above the SMA. It is +0.0018 within 20 bars of the cross (n 213), +0.0020 at 20–60 bars (n 133) and +0.027 at 60–150 bars (t 0.71, n 53). The plan's "fresh cross" bars carry nothing.
- **F7:** Coins are mixed. Block means are +0.23 for BTC (t 1.69) and +0.37 for ZEC (t 1.27) but −0.096 for XMR (t −1.00), so no single coin's effect is clear.

## Ideas
- `002-03_price-cross-above-long-sma.b1_above-average-with-momentum` (from F4, F5, F3, F1): While a coin's close sits above its 200-day simple moving average, the further above it sits relative to its own past distances, the larger its rise over the following weeks, only while the close has also risen over the preceding weeks.
- `002-03_price-cross-above-long-sma.b2_persistence-of-time-above` (from F6, F1, F3): The longer a coin's close has stayed above its 200-day simple moving average since crossing it, the larger its rise over the following weeks.
- `002-03_price-cross-above-long-sma.b3_right-tail-trend-continuation` (from F2, F1, F4): While a coin's close sits above its 200-day simple moving average, its rises over the following weeks are larger than its falls, the more so the further above the average it sits.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
