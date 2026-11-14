---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day SMA is above the 200-day SMA, the coin keeps rising, and the rise is larger the closer its close sits to its recent high, only while price trades near that high rather than deep below it.
Consequence: Hold the trend long at full weight when price presses its recent highs and cut it as price sinks from them, which removes the drawdown days that a still-widening spread keeps the book long through.
Why:
- F1: The book falls short of holding on both failed measures: its daily Sharpe is 0.376 against holding's 0.570, its mean daily return is 0.00074 against 0.00121, and its deepest fall is -93.1% against holding's -79.97%, which leaves a Calmar of 0.001.
- F5: The losing state is a spread that is still widening while price has already turned down over 20 bars: on invested days in that state the next-day coin return averages -0.245% (n = 885) and the state carries -33% of the book's gain, while the r20-positive states earn +0.40% and +0.32% per day (t = 2.38 and 2.49).
- F6: The book's deepest falls sit in that state: across windows w12, w13, w16 and w18 (book -23%, -55%, -35% and -60%), invested days with a falling 20-bar return and a widening spread average -1.45% per day (t = -2.13, n = 168), and 12.5% of those days drop more than 8%.
- F7: Distance from the recent high sorts the gain in the same way: on invested days, when the close is within the top quartile of closeness to its 60-bar high, the next-day return averages +0.48% (t = 3.17) and carries 72% of the gain, while the quartile farthest below the high averages -0.10% and has 6.5% of its days below -8%.
