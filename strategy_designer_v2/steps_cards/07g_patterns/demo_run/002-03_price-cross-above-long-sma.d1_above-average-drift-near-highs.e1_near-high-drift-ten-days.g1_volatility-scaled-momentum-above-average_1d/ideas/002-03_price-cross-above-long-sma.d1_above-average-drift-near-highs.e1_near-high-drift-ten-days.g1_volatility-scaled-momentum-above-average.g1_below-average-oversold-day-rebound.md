---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is below its 200-day average, the larger its one-day fall measured against its 20-day daily volatility, the larger its rise over the next 1 to 2 days.
Consequence: Below the long average, a trader would buy a short-term rebound sized by how outsized the day's fall was relative to recent volatility, and would refuse to sell into such falls.
Why:
- F1: Below the 200-day average (the 'unknown' regime), the next day's excess return falls as the day's own fall, measured against 20-day volatility, gets smaller: the slope on down days is -0.0041 (t -5.39, 3810 cases), while above the average it is -0.0008 (t -0.58, 3246 cases) and on up days it is -0.0001 (t -0.19, 7286 cases).
- F2: The rebound below the average is graded. On those down days, the next-day excess return by quintile of the vol-scaled fall runs +0.72% (t 3.35), +0.37% (t 2.38), +0.07%, -0.21%, -0.14%, with 762 cases in each quintile.
- F3: The rebound holds beyond one day and beyond one year. On a non-overlapping 2-day grid the slope is -0.0035 (t -2.52, 1823 cases), and without 2020 it is -0.0019 (t -2.43, 3552 cases). Even so, 2020 alone is the strongest year (slope -0.0198, t -6.07, 258 cases).
- F4: The slope below the average is negative in all 6 coins and all 8 years. The coins are strongest in XMR (t -3.64) and XRP (t -3.66), and BTC is weakest (t -1.67).
