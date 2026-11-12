---
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3172 USD
---
## Findings
- **F1:** The trend effect is mostly in the large part of the forecast. On bars with a positive forecast, the gross position-weighted next-day return rises across forecast quintiles: −0.000089, 0.000772, 0.000511, 0.003418 and 0.005610. The next-20-bar return rises from −0.0012 in the lowest quintile (mean forecast 1.8) to +0.076 in the highest (mean forecast 20.0). The smallest forecasts, closes just above the 200-day SMA, earn nothing or lose.
- **F2:** Being above the SMA alone adds almost nothing over being below it. Bars with a positive forecast return 0.001337 the next day and 0.0322 over 20 bars, against 0.001239 and 0.0260 for flat bars. The book's gross daily gain (0.001023) is below simply holding the coins (0.001287), which is why the book's Sharpe trails holding's Sharpe by −0.065.
- **F3:** Fees are not the problem; whipsaw is. The 2228 trades, all long, average a 4.23% gain before fees and 4.13% after. Only 29.7% win. The three shorter duration quartiles (about 1.8, 6.5 and 18.1 days held) lose −6.26%, −5.75% and −2.47% before fees. Only the longest quartile (about 58.7 days) earns, at +31.41%.
- **F4:** Above the SMA, the direction of the last 20 days decides the result. On bars with a positive forecast where the close is below its level 20 bars earlier (3701 bars), the gross daily return is −0.000674 and the next-20-bar return is −0.0018. Where it is above (4647 bars), these are +0.004210 and +0.0603.
- **F5:** The losses cluster in the bear years. The gross daily return is −0.000691 in 2018 and −0.000362 in 2022, when the book was long on only 19% and 10% of bars. In 2023 the book lost −0.000198 a day while the coins gained +0.001502. These failed entries during declines drive the poor Calmar of 0.14.
- **F6:** On bars with a positive forecast, the effect is strongest when the coin is volatile. The gross daily return is 0.004720 in the top tercile of 20-day volatility (mean daily volatility 0.070), against 0.001658 and 0.001651 in the calmer two terciles.
- **F7:** The most stretched closes give back their 20-day edge. The top quintile of raw distance above the SMA (mean 110%) has a next-20-bar return of only 0.0120, against 0.0596 for the fourth quintile (mean 41%), even though its next-day return is high at 0.0035.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-with-rising-month` (from F4, F2, F5): When a coin's close is above its 200-day average and also above its close of 20 bars earlier, the coin keeps rising over the next 20 bars by more than its average 20-bar return.
- `002-03_price-cross-above-long-sma.d2_marginal-crosses-whipsaw-back` (from F1, F3): When a coin's close sits only slightly above its 200-day average compared with its usual distance, the price falls back below the average within days more often than it keeps rising.
- `002-03_price-cross-above-long-sma.d3_overstretched-trend-loses-drift` (from F7, F1): When a coin's close is far further above its 200-day average than is usual for that coin, its rise over the next 20 bars is smaller than when it is moderately above.
- `002-03_price-cross-above-long-sma.d4_volatile-uptrends-persist-more` (from F6): When a coin trading above its 200-day average is in a high-volatility stretch, measured by its recent daily return spread, the following days rise more than in calm stretches above the average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
