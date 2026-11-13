---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-03_calm-uptrend-drift
line: 7.b inconclusive
backtest: N3-03_calm-uptrend-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A calm coin with a positive 20-day return drifts up over the next five days only when its close is above its own 200-day moving average, so the drift follows the coin's longer bull trend.
Consequence: A trader would take calm-uptrend longs only while the coin is above its long-term average and would stand aside below it.
Why:
- F2: The result is driven by the market's own direction year by year. Long bars gain strongly in the bull years, 2020 (+3.22%, t 4.44, n 145) and 2021 (+3.42%, t 2.55, n 138). They lose strongly in the bear years, 2018 (−3.11%, t −2.38, n 74) and 2022 (−2.87%, t −3.43, n 114). In 2023 to 2025 they sit near zero (|t| < 0.3, about 100 to 111 cases a year). Opposite signs across years cancel in the pooled t.
- F1: The effect is small and spread thin. On long bars, the mean 5-bar excess return is +0.55% with t = 1.49 over 897 non-overlapping cases. No single coin reaches t = 1.3: LTC is +1.16% (t 1.29, n 159), XRP +1.52% (t 1.05, n 122), BTC +0.01% (t 0.01, n 169) and XMR −0.16% (t −0.25, n 168). Long bars are as noisy as all bars (std of 5-bar return 11.0% against 11.1%).
- F5: Calmness itself adds little. Rising bars outside the calm regime show a similar +0.59% (t 1.27, n 652), close to the calm rising bars in F1.
