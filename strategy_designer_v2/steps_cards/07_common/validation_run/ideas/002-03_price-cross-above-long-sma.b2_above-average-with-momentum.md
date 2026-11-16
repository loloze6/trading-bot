---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close sits above its 200-day simple moving average, the more it rises above its usual drift over the next 20 days, only while its own 20-day return is positive, the larger that return the stronger.
Consequence: A trader would treat a price above the long average as a trend only when the last 20 days confirm it, and not when price is above the average but slipping.
Why:
- F3: The coin's own 20-day return splits the same way: above-average cases with a positive past 20-day return earn +0.033 (n 219, t 1.25), and those with a negative one earn -0.028 (n 180, t -1.75).
- F5: The grading by distance does not order the outcome. Spearman correlation of raw distance with 20-day excess is -0.04. Forecast quartiles run q1 -0.035 (t -1.81), q2 -0.004, q3 -0.013, q4 +0.072 (t 1.34), and q4's mean rests on the tail.
- F1: The result is unclear because a few huge winners carry the mean: on the 399 non-overlapping 20-day cases with forecast > 0, the mean excess return is +0.0052 (t 0.32), but the median is -0.036, the 10% trimmed mean is -0.024, the skew is 7.4, only 40.6% beat holding, and the five largest cases add up to 415% of the summed excess.
