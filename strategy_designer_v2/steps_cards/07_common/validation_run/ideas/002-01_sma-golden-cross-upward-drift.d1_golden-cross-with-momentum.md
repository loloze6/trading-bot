---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day SMA of the close is above the 200-day SMA, the coin keeps drifting upward, and the more so the larger its rise over the recent weeks, only while that recent-weeks return is positive.
Consequence: A trader long on the golden cross would size the position by the coin's recent-weeks rise and stand aside while the coin has been falling under a standing cross, which removes the days that make up the book's deep falls.
Why:
- F1: The book's deep falls happen while it is long into a coin that has been falling, not rising. On the 1856 days with the book more than 20% below its window peak, it was long 89% of the time. On 68% of those days the coin's prior 20-day return was negative (mean -6.95%), against 42% of all long days.
- F2: Being long only pays when the coin has risen over the prior 20 days. Long days with a rising prior 20-day return (4410 days) had a coin mean of 0.003350 a day (t 4.52) and a book mean of 0.001234. Long days with a falling prior 20 days (5591 days) had a coin mean of only 0.000338 (t 0.48) and a book mean of 0.000245, at a similar daily spread (0.0285 against 0.0262).
- F3: When the forecast is positive, the next 10 bars' return above holding rises with the coin's prior 20-bar return: slope 0.103, t 3.74, 694 independent blocks. By quartile of that prior return it runs from -2.94% (t -2.73) in the falling quartile to +3.39% (t 1.83) in the strongest. In flat blocks the same slope is -0.018 (t -0.74).
- F4: The size of the 50/200 spread does not grade the move that follows. Active blocks by raw spread quartile return +0.14%, +1.30%, -0.53% and -0.70% over 10 bars against holding, and the verdict's slope on the forecast has t 0.37. Yet the book puts its largest allocation (0.89) on the top forecast bucket.
- F7: Keeping the book's daily return only on days after a rising 20-day return, and setting it to zero otherwise, lifts the pooled Sharpe from 0.36 to 0.46 but lowers the mean from 0.000400 to 0.000319. So the filter alone cures the falls rather than the low mean.
