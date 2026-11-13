---
line: 7.b inconclusive
backtest: N3-03_calm-uptrend-drift_1d
idea tested: N3-03_calm-uptrend-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2703 USD
---
## Findings
- **F1:** The effect is small and spread thin. On long bars, the mean 5-bar excess return is +0.55% with t = 1.49 over 897 non-overlapping cases. No single coin reaches t = 1.3: LTC is +1.16% (t 1.29, n 159), XRP +1.52% (t 1.05, n 122), BTC +0.01% (t 0.01, n 169) and XMR −0.16% (t −0.25, n 168). Long bars are as noisy as all bars (std of 5-bar return 11.0% against 11.1%).
- **F2:** The result is driven by the market's own direction year by year. Long bars gain strongly in the bull years, 2020 (+3.22%, t 4.44, n 145) and 2021 (+3.42%, t 2.55, n 138). They lose strongly in the bear years, 2018 (−3.11%, t −2.38, n 74) and 2022 (−2.87%, t −3.43, n 114). In 2023 to 2025 they sit near zero (|t| < 0.3, about 100 to 111 cases a year). Opposite signs across years cancel in the pooled t.
- **F3:** The calm-and-falling side is the clearer half. Bars in the calm regime with a 20-day return at or below zero (forecast 0) are followed by a mean 5-bar excess return of −0.66% (t −2.12, n 912). Calm rising bars give +0.55% and all bars give +0.02% (t 0.11, n 3419), so the calm long-minus-flat spread is about 1.2% per 5 bars.
- **F4:** A larger forecast does not mean a larger drift. Forecast quartiles give +0.75%, +0.64%, +0.14% and +0.66% (all |t| < 1, about 224 cases each). By size of the 20-day return, only the second quartile stands out: +2.20%, t 2.45, n 191. The smallest quartile is −0.53% (t −0.88) and the largest +0.34% (t 0.37).
- **F5:** Calmness itself adds little. Rising bars outside the calm regime show a similar +0.59% (t 1.27, n 652), close to the calm rising bars in F1.

## Ideas
- `N3-03_calm-uptrend-drift.b1_calm-downtrend-drifts-lower` (from F3, F1): When a coin's 20-day volatility is in the lower half of its last 100 days and its 20-day return is zero or negative, its price drifts down over the next five days.
- `N3-03_calm-uptrend-drift.b2_calm-drift-inside-bull-trend` (from F2, F1, F5): A calm coin with a positive 20-day return drifts up over the next five days only when its close is above its own 200-day moving average, so the drift follows the coin's longer bull trend.
- `N3-03_calm-uptrend-drift.b3_modest-calm-rise-drifts-up` (from F4): A calm coin whose 20-day return is modestly positive, in the lower-middle part of its usual positive range rather than at its largest, drifts up over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
