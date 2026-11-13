---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-01_trend-with-rising-month
line: 7.b inconclusive
backtest: N1-01_trend-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On BTC, when the daily close is above its 200-day average and above its close of 20 bars earlier, BTC's return over the next 20 bars exceeds its own average 20-bar return.
Consequence: A trader would take the trend-following long on BTC only and refuse it on the altcoins, where it shows nothing or a lag.
Why:
- F3: The effect sits in BTC only. BTC's active cases have a mean 20-bar log excess of +0.039 (t 1.86, n 50, hit 56%), and their median beats the market average (+0.015, hit 62%). XMR (−0.025, t −0.92, n 41), XRP (−0.047, t −0.86, n 36, hit 28%) and LTC (−0.014) are negative. ZEC's +0.13 arithmetic mean rests on a median of −0.023.
- F2: Measured against the six-coin average 20-bar return at the same moment, active cases show no edge: mean +0.0003, t 0.01, n 251, hit 47%. The active coin's forward return has a correlation of 0.54 with that market average, so the market's own moves account for much of what the test measured.
- F1: The positive mean is carried by a few outliers. Over the 251 non-overlapping active 20-bar cases, the mean excess return is +0.015 (t 0.63), but the median is −0.038 and only 43.4% of cases are positive. The skew is 7.3, the 5 best cases sum to 8.37 against a total of 3.77, and the 5%-trimmed mean is −0.015.
