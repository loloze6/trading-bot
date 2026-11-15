---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close sits above its 200-day simple moving average, the more it rises above its usual drift over the next 20 days, only while that 200-day average has itself been rising over the past 20 days, the larger its 20-day rise the stronger.
Consequence: A trader would ride the coin above its long average only when the average itself slopes up, and stand aside when the price is above a falling average.
Why:
- F2: The effect splits on whether the 200-day average itself is rising: above-average cases where the SMA's 20-day change is positive earn +0.026 excess over 20 days (n 266, t 1.17), while those where the SMA is falling earn -0.037 (n 133, t -2.03).
- F4: The two bad years drown the effect: 2018 gives -0.132 (n 21, t -2.76) and 2022 gives -0.173 (n 10, t -3.12), while every other year is between -0.003 and +0.036 (none with |t| > 0.83).
- F1: The result is unclear because a few huge winners carry the mean: on the 399 non-overlapping 20-day cases with forecast > 0, the mean excess return is +0.0052 (t 0.32), but the median is -0.036, the 10% trimmed mean is -0.024, the skew is 7.4, only 40.6% beat holding, and the five largest cases add up to 415% of the summed excess.
