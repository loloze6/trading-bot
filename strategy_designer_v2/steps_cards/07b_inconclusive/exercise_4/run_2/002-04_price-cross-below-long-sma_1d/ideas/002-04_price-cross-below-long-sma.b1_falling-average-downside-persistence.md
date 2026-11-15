---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the coin's close is below its 200-day simple moving average, it keeps falling beyond its usual drift over the next 10 days, the more so the faster that 200-day average has itself declined over the past 20 days.
Consequence: A trader would short coins below their long average only when the average itself is turning down steeply, and size up with the steepness of that decline rather than with the distance below it.
Why:
- F4: The fall shows where the 200-day average itself is falling fastest. The quartile with the steepest 20-day decline of the SMA200 has excess 10-day return -0.0175 (t -1.66, n 173, 54% of blocks down), against -0.0012 (t -0.11) for the quartile where it rises most. Over 20 days the same split gives -0.0159 against +0.0153.
- F2: The effect is mixed across periods and cancels out. Below the SMA200 the excess 10-day return is clearly negative in the bear years: 2018 -0.0395 (t -2.41, n 137), 2019 -0.0158 (t -1.87) and 2022 -0.0250 (t -2.64, n 191). It is clearly positive in the recovery years: 2020 +0.0493 (t 3.05, n 73), 2021 +0.0416 (t 1.75) and 2023 +0.0190 (t 1.67).
- F1: Below the SMA200 the coin's excess 10-day return is only slightly negative, mean -0.0034 (t -0.70, n 841 non-overlapping blocks), against +0.0037 (t 0.61, n 816) above it, and the plan's allocation × excess product stays near zero at every horizon (10 days: -0.00027, t -0.23; 3 to 40 days: |t| ≤ 0.41). The effect is weak overall.
