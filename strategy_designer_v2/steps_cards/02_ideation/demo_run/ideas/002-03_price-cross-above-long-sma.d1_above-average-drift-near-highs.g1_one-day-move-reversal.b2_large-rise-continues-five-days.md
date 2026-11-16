---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day rise relative to the standard deviation of its daily returns over the past 20 days, the larger its further rise over the next 5 days.
Consequence: A trader would keep or add to a long after an unusually large one-day rise rather than fade it.
Why:
- F2: The reversal holds after falls only. Next-day excess return rises with the size of the fall (slope t 3.90, n 8,514 by forecast; t 3.61, n 7,151 by the raw z). After rises, the slope on the forecast is the wrong way (t -2.02, n 8,866), so larger rises are followed by slightly larger rises, not falls.
- F5: After rises, the move continues over longer horizons. The slope of the 5-day excess return on minus z within rises is -0.0109 (t -2.51, n 1,365), and -0.0044 at 3 days (t -1.98, n 2,466): the larger the one-day rise relative to the usual move, the larger the further rise over 5 days.
