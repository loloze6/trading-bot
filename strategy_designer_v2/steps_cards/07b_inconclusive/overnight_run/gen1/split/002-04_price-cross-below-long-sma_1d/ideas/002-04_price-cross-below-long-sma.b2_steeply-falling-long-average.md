---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is below its 200-day SMA and the SMA200 itself has fallen steeply over the prior 20 bars, the coin falls further over the next 10 days than its usual drift.
Consequence: A trader would short below the average only when the average itself is falling steeply, and should treat this as a bet on the whole market falling, not on the coin falling more than the others.
Why:
- F8: Blocks where the SMA200 itself fell most over the prior 20 bars (quartile 0, mean slope -8.9%) gain +0.018 (t = 1.83, n = 199), against -0.002 to +0.001 in the other quartiles. This gain is pure market move: relative to the market it is +0.0002, t = 0.05.
- F3: The sign of the effect flips by year. Short gains were positive in 2018 (+0.039, t = 2.32, n = 134), 2019 (+0.012, t = 1.37) and 2022 (+0.023, t = 2.48, n = 195). They were negative in 2020 (-0.043, t = -2.73, n = 88), 2021 (-0.051, t = -2.32, n = 74) and 2023–2025 (-0.008 to -0.015). Bear-market and rebound years cancel each other.
- F2: The coin's own 10-bar return while short correlates 0.82 with the equal-weight 10-bar return of the six coins, so market moves dominate. Removing the market cuts the standard deviation from 0.140 to 0.079 but leaves no edge: relative short gain is -0.0003, t = -0.10.
