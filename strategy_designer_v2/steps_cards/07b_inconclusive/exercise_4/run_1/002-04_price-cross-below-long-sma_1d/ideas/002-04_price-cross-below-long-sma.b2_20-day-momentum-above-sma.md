---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose close is above its 200-day simple moving average rises beyond its usual drift over the next 10 days, the more so the larger its 20-day return.
Consequence: A trader would size longs above the long average by the strength of the recent 20-day rise rather than by the cross itself.
Why:
- F5: The 20-day return separates outcomes far more than the SMA does, on the side above the average. When the close was above the 200-day SMA, a positive 20-day return was followed by a 10-day excess return of +0.0207 (t +2.36, n 455), and a negative one by -0.0176 (t -1.91, n 231).
- F6: Below the SMA, the fall was larger after a positive 20-day return than after a negative one: -0.0111 (t -1.23, n 234) against -0.0032 (t -0.54, n 455). Together with F5, the short-term move matters more than the distance below the average.
- F3: The plan's grading runs the wrong way. The deepest quarter of forecasts was followed by +0.0076 over 10 days (t +0.71, 48.8 % down), while the three shallower quarters were followed by -0.0059 to -0.0080 (t -0.66 to -0.84). The step-5 slope of excess return on allocation was -0.0126, not positive.
