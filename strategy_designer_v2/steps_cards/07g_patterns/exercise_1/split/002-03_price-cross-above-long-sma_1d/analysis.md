---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.4196 USD
---
## Findings
- **F1:** The book's whole profit comes from trades held longer than 30 days. Those 515 trades averaged +33.8% net, won 69.7% of the time and summed to +17,412%, against a total book P&L of +9,206%. Every shorter bucket lost on average: 241 trades of 1 day or less averaged −6.26% with a 1.2% win rate, 332 trades of 1–3 days averaged −6.54% (4.5% win rate), 526 trades of 3–10 days averaged −5.77% and 611 trades of 10–30 days averaged −2.44%. These short trades are 1,710 of the 2,228 trades, all of them long.
- **F2:** Bars just above the 200-day SMA (forecast 0–5, n=1,909) had a mean next-20-bar return of −0.25%, a median of −1.65% and a 38.8% hit rate. Flat bars (n=7,297) had +2.60% mean and 43.0% hit. The 15–20 forecast bucket had +6.30% mean but a −0.11% median and 40.0% hit, so the edge from a larger distance is in the mean only.
- **F3:** Forward 20-bar returns while long are strongly right-skewed. Long bars had skew 4.30 (mean +3.22%, median −0.53%), against skew 1.23 when flat (mean +2.60%, median +0.60%). In raw distance, the top decile (mean 108% above the SMA, 20-day vol 0.064) had a −2.40% median and a 37.5% hit rate, the lowest of all deciles.
- **F4:** Whether being above the SMA helped depended on 20-day momentum. Long bars in the bottom 20-day-momentum quintile (≤ −13.9%) returned −4.75% over the next 20 bars, against +2.74% for flat bars in the same quintile. Long bars in the top two quintiles returned +5.56% and +6.54%, against +1.61% and +3.11% for flat bars.
- **F5:** Time spent in a state matters on both sides. Bars that had been below the SMA for 60–150 days returned −1.29% over 20 bars with a 32.5% hit rate (n=1,492). Bars below for 5–60 days returned +3.95% to +4.36% with hits of 47–48%. Bars above for 60–150 days had a +6.01% mean but only a 34.3% hit rate.
- **F6:** The cross events themselves show little continuation. After an upward cross (n=278), the next 5 bars returned +0.05% and the next 20 returned +2.47% (median +1.57%, hit 44.6%). After a downward cross (n=280), the next 5 bars returned +0.92%, a short-term bounce, while the next 20 had a +1.09% mean but a −1.30% median and a 39.6% hit rate.
- **F7:** Saturday is a positive return day across the sample. Pooled Saturday daily return was +0.44% (t=5.41), with positive t in all six coins (1.40 to 2.92) and t≥2.8 in 2019, 2020, 2024 and 2025. It was not positive in 2022 (t 0.42) or 2023 (t −0.01). On long bars the book earned +0.86% on Saturdays (t 4.43) and +0.63% on Fridays (t 3.52), against −0.42% on Tuesdays (t −2.24) and −0.41% on Thursdays (t −2.12).
- **F8:** Large daily moves partly reverse the next day. After a drop of 2 standard deviations or more (n=366), the next day averaged +1.78% and the next 5 days +1.97%. After a rise of more than 2 standard deviations (n=495), the next day averaged −0.52%. After ordinary days (within ±1 sd), the next day averaged +0.05%.
- **F9:** The long-versus-flat edge disappears in high volatility. Next-20-bar return for long bars minus flat bars was +2.25 points in the low 20-day-vol tercile and +2.56 points in the middle tercile, but −0.01 points in the high tercile (3.20% vs 3.21%). Even so, the book's mean daily return on long high-vol bars was the largest of the three (+0.40% vs +0.15% in the low tercile).
- **F10:** The signal's value flips by year and by coin. Long bars underperformed flat bars over 20 bars in 2018 (−17.0% vs −6.9%), 2020 (+6.4% vs +16.0%), 2021 (+4.8% vs +12.4%) and 2022 (−9.2% vs −0.9%), and outperformed in 2019 and 2025. ZEC long bars returned +8.2% vs +2.5% flat, while XRP long bars returned +4.1% vs +7.9% flat and LTC +0.6% vs +0.9%.
- **F11:** The book's extreme days fall in stretched, high-vol conditions. The best 1% of book days (mean +26.7%) came at a mean distance of 132% above the SMA after +71% 20-day momentum. The worst 1% (mean −21.9%) came at 80% above after +27% momentum. Both had 20-day vol of about 0.073 against 0.042 on other days. The top 5% of book days account for 2.9× to 16.5× the net book sum per coin, and for XMR the net is near zero or negative (share −96.5).

## Ideas
- `002-03_price-cross-above-long-sma.g1_above-average-weak-momentum-decline` (from F4, F11): When a coin closes above its 200-day average and its own 20-day return is strongly negative, the coin keeps falling over the next 20 bars. It does worse than it does on bars below the average with the same weak momentum.
- `002-03_price-cross-above-long-sma.g2_above-average-strong-momentum-continuation` (from F4, F9): When a coin closes above its 200-day average and its own 20-day return is among its strongest, the coin rises further over the next 20 bars than it does at other times.
- `002-03_price-cross-above-long-sma.g3_marginal-cross-whipsaw-drift-lower` (from F2, F6, F1): When a coin's close sits only slightly above its 200-day average, the next 20 bars more often end lower than the coin's usual drift. This holds most often in the weeks right after an upward cross.
- `002-03_price-cross-above-long-sma.g4_stretched-above-median-decline` (from F3, F2, F11): When a coin's close sits very far above its 200-day average with high recent volatility, the typical next-20-bar outcome is a decline. The average is held up only by a few very large further rallies.
- `002-03_price-cross-above-long-sma.g5_prolonged-below-continued-weakness` (from F5): When a coin has stayed below its 200-day average for a long stretch of months, it keeps falling over the next 20 bars more often than it rises.
- `002-03_price-cross-above-long-sma.g6_fresh-break-below-rebound` (from F5, F6): When a coin has recently dropped below its 200-day average, within the past several weeks, it rises over the next 20 bars more than its usual drift. The rise starts with a short bounce in the first days after the cross down.
- `002-03_price-cross-above-long-sma.g7_large-drop-next-day-rebound` (from F8): After a coin closes with a daily drop that is large relative to its own recent volatility, the next day's close is higher on average.
- `002-03_price-cross-above-long-sma.g8_large-rise-next-day-giveback` (from F8): After a coin closes with a daily rise that is large relative to its own recent volatility, the next day's close is lower on average.
- `002-03_price-cross-above-long-sma.g9_saturday-positive-drift` (from F7): A coin's Saturday close-to-close return is positive on average, and this holds for every coin in the sample.
- `002-03_price-cross-above-long-sma.g10_calm-regime-above-average-edge` (from F9): When a coin closes above its 200-day average while its 20-day volatility is in its low or middle range, it rises more over the next 20 bars than when it is below the average at the same volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
