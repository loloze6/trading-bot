---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is above its 200-day average, it rises more than its usual drift over the next 20 days, but only while its 60-day return is positive, and the larger that 60-day return, the larger the rise.
Consequence: A trader would hold a coin above its 200-day average only when its last 60 days are up, sized by the strength of that rise, and stay out when it sits above the average after a flat or falling 60 days.
Why:
- F1: When the close sits above its 200-day average, the coin barely beats holding over the next 20 days and the typical case does worse: mean excess +0.0052 (t 0.32, 399 non-overlapping cases), median −0.036, only 40.6% of cases beat holding, and the 5%-trimmed mean is −0.018.
- F4: The sign changes across coins and years. At 20 days, BTC (+0.013), LTC (+0.008) and ZEC (+0.059) are positive, while ETH (−0.007), XMR (−0.012) and XRP (−0.022) are negative. The years 2018 (−0.132, t −2.76) and 2022 (−0.173, t −3.12) are strongly negative, while 2020, 2021, 2024 and 2025 are mildly positive.
- F5: The effect depends on the coin's 60-day return. When the 60-day return is zero or negative, the 20-day excess is −0.056 (t −1.53, n 31). When it is positive, the excess is +0.020 (t 0.97, n 165) and rises with the 60-day return: +0.012 for 0–20%, +0.016 for 20–50% and +0.036 above 50%. Within the positive-60-day cases, five of six coins are positive.
