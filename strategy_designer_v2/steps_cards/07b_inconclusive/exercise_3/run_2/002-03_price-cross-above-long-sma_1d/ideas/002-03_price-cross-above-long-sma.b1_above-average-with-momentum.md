---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits above its 200-day simple moving average, the further above it sits relative to its own past distances, the larger its rise over the following weeks, only while the close has also risen over the preceding weeks.
Consequence: A trader would hold above-average coins mostly when price is also rising into the reading, and stand aside when it sits above the average after a recent fall.
Why:
- F4: Only the largest standardised forecasts carry a gain. The top forecast quartile gives +0.072 (t 1.34, n 100) and the bottom quartile −0.035 (t −1.81, n 100), with the middle two near zero (−0.004, −0.013). Raw-distance sextiles show no order (+0.0125 and +0.0128 for the two highest, −0.015 just above the SMA).
- F5: Prior momentum separates the cases. Among forecast > 0 bars, the lowest 20-bar momentum tercile gives −0.022 (t −1.13), the middle +0.025 (t 1.34) and the highest +0.042 (t 0.85), each n 110.
- F3: The effect splits by period. Forecast > 0 bars lost heavily in 2018 (−0.132, t −2.76, n 21) and 2022 (−0.173, t −3.12, n 10). They earned in 2020 (+0.022), 2024 (+0.021) and 2025 (+0.036), and 2020's blocks reached +0.46 (t 2.03). The above-SMA state reverses in bear years and persists in bull years.
- F1: Bar by bar the effect is close to zero. On the non-overlapping 20-bar grid, bars with forecast > 0 beat the coin's pooled mean by 0.0052 (t 0.32, n 399), against −0.00015 (t −0.01, n 412) for bars below the SMA. Only 40.6% of them win, and the median is −0.036. No horizon from 5 to 60 bars gets past |t| 0.61.
