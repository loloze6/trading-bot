---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close has stayed above its 200-day SMA for at least 30 consecutive bars, its return over the next 20 bars beats its own average drift.
Consequence: A trader would treat a close above the average as a long only once that trend has lasted, not right after the cross.
Why:
- F4: Time since the cross works against the brief's "new trend" reading: the first 10 bars above the SMA give -0.011 (t -1.96, n 1953) and bars 10-30 give -0.002 (t -0.27), while bars 30-60 give +0.016 (t 2.40) and bars 60-120 give +0.035 (t 4.57).
- F6: The effect depends on the period: active blocks lost in 2018 (mean -1.92, t -3.33) and 2022 (-0.60, t -2.01) and were positive but not significant in 2020, 2024 and 2025 (t 1.31, 1.33, 1.07); bar-level hit rates were only 17-18% in 2018 and 2022, against 54% in 2020.
