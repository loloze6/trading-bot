---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3527 USD
---
## Findings
- **F1:** A coin's next-day excess return falls steadily as its one-day move, scaled by its prior 20-day volatility, rises. The bottom decile of scaled moves is followed by +0.55% (t=3.67, n=1378, hit 58.5%) and the second decile by +0.26% (t=2.08). Deciles 3 to 9 are flat to negative (−0.22% at decile 7, t=−1.91). The regression slope of the next-day return on the scaled move is −0.0014 (p=0.00008, about 9,600 bars).
- **F2:** The rebound after the largest scaled falls appears in every coin, though only XMR is individually significant: BTC +0.17% (t=0.92), ETH +0.30%, LTC +0.33%, XMR +0.76% (t=3.70), XRP +0.39% and ZEC +0.48% (t=1.76). It is positive in 6 of 8 years and strongest in 2020 (+1.21%, t=3.30) and 2021 (+1.12%, t=3.38). It fades to zero in 2024 (+0.00%) and 2025 (−0.03%).
- **F3:** The rebound after the bottom two deciles of scaled falls is larger when the close is below its 200-day SMA (+0.54%, t=4.13, n=1543) than above it (+0.24%, t=1.61, n=1213). A 3-day version on the non-overlapping 3-day grid still shows +0.86% after bottom-decile falls (t=2.08, n=452).
- **F4:** The idea's own signal is weak and its gain is lopsided. Grid bars with forecast 15 to 20 earn +5.5% excess over 20 days, but with t=1.17 (n=113). Forecast 0 to 5 earns −2.9% (t=−1.63). Only 40.6% of forecast > 0 bars beat holding over 20 days, and the octiles of distance above the SMA show no monotone pattern (t between −0.8 and 0.7).
- **F5:** The book's profit comes from a few long trades. The longest-duration quintile of trades (median 62 days) averages +40.7% with 72% winners. The shortest quintile (median 1 day) averages −6.0% with 2.8% winners, and the next quintile (4 days) averages −4.6%. This is the convex payoff of a trend filter, not a 20-day drift.
- **F6:** Next-day returns vary by weekday, but the pattern is not stable enough to act on. Friday is +0.28% (t=3.47) and stays so on mid-sized prior moves (+0.29%, t=2.83), but it is negative in 2018 (−0.50%) and 2023 (−0.13%). Wednesday is −0.30% (t=−2.72), but the effect is concentrated in 2019 (−1.36%, t=−5.79). With seven weekdays tested and no grading possible, this suggests no idea.

## Ideas
- `002-03_price-cross-above-long-sma.g1_volatility-scaled-one-day-fall-rebound` (from F1, F2, F3): The larger a coin's one-day fall relative to its own past 20-day daily volatility, the more it rises above its average return over the next 1 to 3 days.
- `002-03_price-cross-above-long-sma.g2_downtrend-oversold-day-rebound` (from F1, F3): While a coin's close is below its 200-day average, the larger its one-day fall relative to its past 20-day daily volatility, the larger its rise above its average return over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
