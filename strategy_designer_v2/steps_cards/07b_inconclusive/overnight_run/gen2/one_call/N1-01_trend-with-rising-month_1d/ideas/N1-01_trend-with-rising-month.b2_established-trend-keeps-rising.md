---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-01_trend-with-rising-month
line: 7.b inconclusive
backtest: N1-01_trend-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin has been in the trending state (close above its 200-day average and above its close of 20 bars earlier) for 11 to 40 consecutive bars, its next 20-bar return exceeds its own average 20-bar return.
Consequence: A trader would wait for the trend state to have lasted about two weeks before buying, rather than entering on its first bars.
Why:
- F6: Regime age matters slightly. Cases 1–10 bars into the trending regime average −0.014 (t −0.76, n 147), while those 11–40 bars in average +0.033 (t 1.10, n 94).
- F1: The positive mean is carried by a few outliers. Over the 251 non-overlapping active 20-bar cases, the mean excess return is +0.015 (t 0.63), but the median is −0.038 and only 43.4% of cases are positive. The skew is 7.3, the 5 best cases sum to 8.37 against a total of 3.77, and the 5%-trimmed mean is −0.015.
