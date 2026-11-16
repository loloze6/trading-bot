---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to the standard deviation of its daily returns over the past 20 days, the larger its rise over the next day.
Consequence: A trader would buy a coin after an unusually large one-day fall, in proportion to the fall, and hold it for one day, rather than sell into the fall.
Why:
- F1: The idea's own forecast predicts the next day on the predicted side, with a pooled slope t of 4.24 over 17,380 bars and a raw-z slope t of 4.74. The test is inconclusive because the timing gain is measured on the book after fees: before fees the position earned 0.000573 a day, but fees took 0.000725 a day at a turnover of 0.66 per bar, leaving -0.000157 a day.
- F2: The reversal holds after falls only. Next-day excess return rises with the size of the fall (slope t 3.90, n 8,514 by forecast; t 3.61, n 7,151 by the raw z). After rises, the slope on the forecast is the wrong way (t -2.02, n 8,866), so larger rises are followed by slightly larger rises, not falls.
- F3: In the book, the long side after falls carries the timing gain, at 0.001095 a day against 0.000122 on the short side after rises. The top forecast deciles 8 and 9, the largest falls, have next-day excess returns of +0.0037 (t 3.14) and +0.0047 (t 3.60).
- F4: The rebound after falls is a one-day effect. Its slope t drops from 3.61 at 1 day to 1.12 at 3 days (n 2,245) and 0.65 at 5 days (n 1,476). It is stronger when the coin is below its 50-day average (t 2.68, n 2,888) than above it (t 1.45, n 2,197).
