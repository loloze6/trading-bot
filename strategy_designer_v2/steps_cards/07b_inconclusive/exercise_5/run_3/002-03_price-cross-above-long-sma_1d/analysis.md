---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3319 USD
---
## Findings
- **F1:** The effect is weak and mostly carried by a few large blocks: the block-mean excess is 0.126 with t 1.73 over 811 blocks, but the median block is 0.0 and only 23.4% of blocks are positive; on the 399 active 20-day grid bars the mean excess is +0.0052 (t 0.32) against −0.0002 on 412 flat bars (active minus flat +0.0053, Welch t 0.27), and only 40.6% of active bars beat the coin's average.
- **F2:** The rising or falling of the 200-day average splits the active bars into two opposite groups: with the average up over the past 20 days the next-20-day excess is +0.026 (t 1.17, n 266), with it down it is −0.037 (t −2.03, n 133); over all bars the excess climbs from −0.020 in the steepest-falling slope quintile to +0.034 and +0.019 in the two rising quintiles (n 134 each).
- **F3:** The result is a mix of opposite years: active bars lost in 2018 (−0.132, t −2.76, n 21) and 2022 (−0.173, t −3.12, n 10), which were falling-average bear years, while blocks earned in 2020 (+0.46, t 2.03) and were positive in 2024 and 2025 (+0.36 and +0.31).
- **F4:** Being above the average does not carry the effect, and fresh crosses do not continue: raw-distance quintiles at 20 days are flat (+0.002, +0.004, −0.007, +0.008, +0.006, all |t| < 0.5), and active bars in the first 20 days after a cross average −0.008 (n 95) and 20–60 days −0.020 (n 62), so the plan's "after the cross" situation shows nothing.
- **F5:** Only the largest forecasts lean positive: the top forecast quartile gives +0.072 (t 1.34, n 100) and the bottom −0.035 (t −1.81, n 100), and low-volatility active bars do best (+0.027, t 1.19) against high-volatility ones (−0.011).
- **F6:** Most of the book's gain is the market's own rise, not timing: the mean daily return is 0.000554, of which the market part is 0.000352 (mean allocation 0.272 × coin mean daily 0.001294), leaving 0.000202 for timing.
- **F7:** Coins disagree: block means are +0.37 for ZEC (t 1.27) and +0.23 for BTC (t 1.69), but −0.096 for XMR (t −1.00) and near zero for ETH and LTC (+0.028, +0.024).

## Ideas
- `002-03_price-cross-above-long-sma.b1_above-rising-long-average` (from F2, F3, F4): While a coin's close is above its 200-day simple moving average, the further it sits above, the more it rises beyond its usual drift over the next 20 days, only while that 200-day average has itself risen over the past 20 days.
- `002-03_price-cross-above-long-sma.b2_long-average-slope-persists` (from F2, F4, F6): The steeper a coin's 200-day simple moving average has risen over the past 20 days, the more the coin rises beyond its usual drift over the next 20 days.
- `002-03_price-cross-above-long-sma.b3_calm-above-long-average` (from F5, F1): While a coin's close is above its 200-day simple moving average, the further it sits above, the more it rises beyond its usual drift over the next 20 days, only while its 60-day volatility is low compared with its own past.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
