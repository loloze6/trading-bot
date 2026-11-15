---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is below its 200-day simple moving average, it falls further than its usual drift over the next 10 days, only while the 200-day average itself has been falling over the past 30 days, and the steeper that fall of the average, the larger the move.
Consequence: A trader would keep below-average shorts only while the long average itself is falling steeply, and would stand aside when the average is flat or rising.
Why:
- F2: The effect is mixed across periods rather than small and uniform: the 10-day short excess gain is positive in 2018 (+0.040, t 2.41, n 137), 2019 (+0.016, t 1.87) and 2022 (+0.025, t 2.64, n 191), and negative in 2020 (-0.049, t -3.05, n 73), 2021 (-0.042, t -1.75), 2023 (-0.019) and 2024 (-0.015), so the years cancel each other in the pooled t of -0.23.
- F3: The years in which the short works are the sustained bear years. Consistent with that, the 10-day short excess gain is largest when the 200-day SMA itself has fallen most over the past 30 days: +0.0166 (t 1.74, n 205) in the steepest-falling tercile (mean SMA change -12 %), against +0.0035 (t 0.42) in the middle tercile and -0.0007 (t -0.07) where the SMA is rising.
- F1: The short gain beyond holding is close to zero at every horizon while the close is below the 200-day SMA (non-overlapping blocks: 1 day t -0.10 on 8674 cases, 5 days t -0.39 on 1709, 10 days t -0.70 on 841, 20 days t -0.01 on 412, 40 days t +0.26 on 197), so the test did not miss the effect by using the wrong horizon.
