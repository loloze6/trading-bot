---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3086 USD
---
## Findings
- **F1:** When the close sits above its 200-day average, the coin barely beats holding over the next 20 days and the typical case does worse: mean excess +0.0052 (t 0.32, 399 non-overlapping cases), median −0.036, only 40.6% of cases beat holding, and the 5%-trimmed mean is −0.018.
- **F2:** That small positive mean rests on a few extreme up-moves: skew is 7.4, the five largest cases sum to 4.1 times the total of all 399, and without ZEC the mean turns to −0.0035 (t −0.29).
- **F3:** The plan's grading does not hold. By distance above the average, the four quartiles give mixed means (+0.005, −0.019, +0.031, +0.004) with all medians negative. Only the top forecast quartile is positive (+0.072, median −0.015), against −0.035, −0.004 and −0.013 for the other three.
- **F4:** The sign changes across coins and years. At 20 days, BTC (+0.013), LTC (+0.008) and ZEC (+0.059) are positive, while ETH (−0.007), XMR (−0.012) and XRP (−0.022) are negative. The years 2018 (−0.132, t −2.76) and 2022 (−0.173, t −3.12) are strongly negative, while 2020, 2021, 2024 and 2025 are mildly positive.
- **F5:** The effect depends on the coin's 60-day return. When the 60-day return is zero or negative, the 20-day excess is −0.056 (t −1.53, n 31). When it is positive, the excess is +0.020 (t 0.97, n 165) and rises with the 60-day return: +0.012 for 0–20%, +0.016 for 20–50% and +0.036 above 50%. Within the positive-60-day cases, five of six coins are positive.
- **F6:** Other horizons do not clarify it. The difference between above-average and flat cases is +0.002 at 5 days, +0.007 at 10, +0.005 at 20, −0.016 at 40 and +0.059 at 60, all with |t| below 1. Most of the book's mean daily gain comes from the market's own rise (0.000345 market part against 0.000209 timing, out of 0.000554).

## Ideas
- `002-03_price-cross-above-long-sma.b1_above-average-with-60-day-momentum` (from F1, F4, F5): When a coin's close is above its 200-day average, it rises more than its usual drift over the next 20 days, but only while its 60-day return is positive, and the larger that 60-day return, the larger the rise.
- `002-03_price-cross-above-long-sma.b2_strongest-above-average-cases-only` (from F2, F3): When a coin's close is above its 200-day average, it rises more than its usual drift over the next 20 days, only in the cases where its close sits furthest above that average relative to its own past distances.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
