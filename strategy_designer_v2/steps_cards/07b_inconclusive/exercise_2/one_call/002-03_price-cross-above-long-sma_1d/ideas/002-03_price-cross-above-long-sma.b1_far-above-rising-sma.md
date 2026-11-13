---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits well above its 200-day SMA and that SMA has itself risen over the last 20 bars, the coin's return over the next 20 bars beats its own average 20-bar return.
Consequence: A trader would keep the long only while the long average is rising and price is well above it, and refuse it otherwise.
Why:
- F2: The effect splits by the direction of the 200-day SMA's own 20-bar slope combined with forecast strength. With the SMA rising and the forecast above 10, the mean excess is +0.074 (t 1.77, n 131, hit 44%). With the SMA falling and the forecast above 10, it is -0.058 (t -2.05, n 57, hit 35%). The weak-forecast cells are both about -0.02 (t -0.91 and -1.21).
- F5: The weighting by forecast size only half works. The top forecast bucket (15 to 20) averages +0.055 (t 1.17), against -0.029 (t -1.63) in the 0 to 5 bucket. Raw distance quartiles show no order (means +0.005, -0.019, +0.031, +0.004).
- F3: The effect depends heavily on the period. With the SMA rising, active samples gained in 2020 (+0.100, t 2.59, hit 59%) and 2021 (+0.102, t 2.34, hit 54%). They lost in 2018 (-0.136, t -2.23) and 2019 (-0.091, t -2.42), and were flat in 2023 to 2025 (t between -0.38 and 0.36). Across the 24 windows, the active mean ranges from -0.37 to +0.27, with a median of -0.036.
