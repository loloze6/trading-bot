---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3405 USD
---
## Findings
- **F1:** The forecast's grading only half shows at 20 days. Excess returns over 20 x the coin's mean daily return rise with the forecast: 0-5 gives −0.029 (t −1.63, n 111), 5-10 gives −0.011 (t −0.54, n 100), 10-15 gives +0.002 (t 0.08, n 75) and 15-20 gives +0.055 (t 1.17, n 113). But the Spearman correlation of forecast with excess is only 0.043 (n 399), and it is 0.018 to 0.060 at 5, 10, 40 and 60 days, so no horizon shows a clear effect.
- **F2:** The positive mean comes from a few large rallies, not from persistence. On forecast > 0 bars the hit rate is below 50% in every forecast bin (0.37 to 0.42 at 20 days), and the median of the allocation-weighted excess is negative for every coin (−0.002 to −0.023) while the means are mostly positive.
- **F3:** Being above the 200-day average adds nothing over being below it. The 20-day excess is 0.0053 higher above than below (Welch t 0.27, n 399 vs 412), and the quintiles of the raw distance all sit between −0.007 and +0.008.
- **F4:** The effect is small and of mixed sign in every coin. Per-coin 20-day excess on forecast > 0 bars runs from −0.022 (XRP) to +0.059 (ZEC), with every |t| ≤ 0.67, so no coin carries it.
- **F5:** Two bear years drag it down. Forecast > 0 bars in 2018 (−0.132, t −2.76, n 21) and 2022 (−0.173, t −3.12, n 10) lose heavily, while 2019-2021 and 2023-2025 sit between −0.003 and +0.036 with t below 0.9.
- **F6:** Volatility splits the effect, but not significantly. Above-average bars in the lowest third of 60-day volatility earn +0.022 (t 1.12, n 86), against +0.003 (mid, n 46) and −0.007 (high, n 64), with a hit rate of 0.36 in high volatility. The vol-target sizing puts 0.87 allocation in low volatility versus 0.36 in high, which is part of why the weighted measure reached t 1.73.
- **F7:** The book earns less than holding. Its mean daily return is 0.00055 against 0.00129 for holding the coins.

## Ideas
- `002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins` (from F1, F4, F2): When a coin's close sits above its 200-day simple moving average, the further above it sits, the more the coin rises over the next 20 days compared with its usual 20-day move. This is the tested idea unchanged, on more coins.
- `002-03_price-cross-above-long-sma.b2_above-average-in-calm-markets` (from F6, F5, F1): When a coin's close sits above its 200-day simple moving average, the further above it sits, the more the coin rises over the next 20 days compared with its usual 20-day move, only while the coin's 60-day volatility of daily returns is low compared with its own past.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
