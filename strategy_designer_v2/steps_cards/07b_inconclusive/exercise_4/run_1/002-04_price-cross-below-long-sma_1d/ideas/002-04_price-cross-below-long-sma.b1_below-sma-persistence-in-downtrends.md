---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose close sits below its 200-day simple moving average keeps falling beyond its usual drift over the next 10 days, the more so the further below it sits, only while its 200-day average has itself been falling over the past 20 days.
Consequence: A trader would short closes below the long average only while that average is declining, and refuse the short in recoveries, when the average has turned up.
Why:
- F2: The effect is strongly mixed by period, and the periods cancel in the pooled t. The 10-day excess return after closes below the SMA was -0.0395 in 2018 (t -2.41, n 137), -0.0158 in 2019 (t -1.87, n 136) and -0.0250 in 2022 (t -2.64, n 191). It was +0.0493 in 2020 (t +3.05, n 73), +0.0416 in 2021 (t +1.75, n 66) and +0.0190 in 2023 (t +1.67, n 84). Persistence held in the long bear years and turned into reversal in the recovery years.
- F4: Across coins the sign is mostly but weakly on the idea's side. Five of six coins had a negative 10-day excess return below the SMA, from -0.0034 (ETH) to -0.0095 (BTC, t -0.95). XRP was +0.0083 (t +0.58), and no coin reached |t| 1.
- F1: The tested effect is near zero at every horizon, not only at the plan's 10 days: closes below the 200-day SMA were followed by a mean excess return of -0.00005 over 1 day (t -0.10, n 8674), -0.00094 over 5 days (t -0.39, n 1709), -0.0034 over 10 days (t -0.70, n 841, 52.6 % down), -0.0002 over 20 days (t -0.01, n 412) and +0.0058 over 40 days (t +0.26, n 197). The plan did not miss a horizon where the effect shows.
