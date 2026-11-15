---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's close has stayed above its 200-day simple moving average, up to about five months, the more it rises above its usual drift over the next 20 days.
Consequence: A trader would add to a trend that has held above its long average for months, rather than buying the fresh cross.
Why:
- F6: Freshly crossed cases do not drift up, but long-established ones do. Within 20 days of the cross the excess is -0.008 (n 95), at 21-60 days it is -0.020 (n 62), and at 61-150 days it is +0.137 (n 10, t 1.66, hit 60%).
- F1: The result is unclear because a few huge winners carry the mean: on the 399 non-overlapping 20-day cases with forecast > 0, the mean excess return is +0.0052 (t 0.32), but the median is -0.036, the 10% trimmed mean is -0.024, the skew is 7.4, only 40.6% beat holding, and the five largest cases add up to 415% of the summed excess.
