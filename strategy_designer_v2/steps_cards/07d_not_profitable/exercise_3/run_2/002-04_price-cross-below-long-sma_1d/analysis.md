---
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
idea tested: 002-04_price-cross-below-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3257 USD
---
## Findings
- **F1:** The book loses its gain to the coin's drift and not to fees: it is short on 57.3% of bars, and on those bars the coin still rises +0.00115 a day, close to its pooled mean of +0.00129 and against +0.00147 on flat bars, so short bars earn -0.000444 a day; the whole book's gross gain is -0.000255 a day against fees of only -0.000026 a day.
- **F2:** The book's falls are rallies it was short into: its worst 5% of 20-day segments (41 cases) lost -14.8% on average while the coin rose +21.8%, and the coin was up in 92.7% of them; in its best segments the coin fell -17.0%.
- **F3:** The deepest forecasts carry the largest short and the worst result: at forecast -15 to -20 the mean allocation is -0.84, the mean gain is -0.0154 (t -1.32, n 125) and the coin's excess 10-bar return is +2.15%, a reversal. At forecast -5 to -15 the shorts gain +0.0048 (t 0.86, n 169) and +0.0028 (t 0.92, n 275).
- **F4:** Shorts lose after a sharp, deep fall and gain after a pause or bounce under the average. In the most negative 20-bar momentum quartile (below -15%) the gain is -0.0047 with excess +0.46%; in the two highest quartiles it is +0.0055 (t 1.29) and +0.0032 (t 1.51). When the close is more than 34% under its 60-bar high the gain is -0.0065 with excess +1.57%; between 9% and 34% under it the gain is +0.0025 and +0.0091 (t 1.39).
- **F5:** The losses gather in recovery years and the gains in bear years. Mean gain per block is -0.0184 in 2020 (t -3.26, n 87), -0.0108 in 2021 (t -2.65) and -0.0110 in 2023 (t -2.13). It is +0.0125 in 2018 (t 1.59), +0.0061 in 2019 (t 2.02) and +0.0080 in 2022 (t 1.42).

## Ideas
- `002-04_price-cross-below-long-sma.d1_below-average-fall-not-stretched` (from F2, F3, F4, F1): While a coin's close sits below its long moving average, the coin keeps falling, more the further it sits below, except when the close has already fallen sharply and far beneath its recent high, where it rebounds more strongly the deeper and faster that fall was.
- `002-04_price-cross-below-long-sma.d2_failed-rally-under-average` (from F4, F2, F3): While a coin's close sits below its long moving average, the coin keeps falling, more the further it sits below, only after it has stopped falling over recent bars or rebounded towards the average: the stronger that recent rebound under the average, the larger the fall that follows.
- `002-04_price-cross-below-long-sma.d3_stretched-fall-rebounds` (from F3, F4, F5): (new idea) After a coin's close has fallen sharply and far below its recent high, the coin rises over the following bars, and it rises more the deeper and faster that fall was.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
