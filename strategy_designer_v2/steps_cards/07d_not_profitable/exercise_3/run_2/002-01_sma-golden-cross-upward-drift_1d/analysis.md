---
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3472 USD
---
## Findings
- **F1:** The book's deep falls happen while it is long into a coin that has been falling, not rising. On the 1856 days with the book more than 20% below its window peak, it was long 89% of the time. On 68% of those days the coin's prior 20-day return was negative (mean -6.95%), against 42% of all long days.
- **F2:** Being long only pays when the coin has risen over the prior 20 days. Long days with a rising prior 20-day return (4410 days) had a coin mean of 0.003350 a day (t 4.52) and a book mean of 0.001234. Long days with a falling prior 20 days (5591 days) had a coin mean of only 0.000338 (t 0.48) and a book mean of 0.000245, at a similar daily spread (0.0285 against 0.0262).
- **F3:** When the forecast is positive, the next 10 bars' return above holding rises with the coin's prior 20-bar return: slope 0.103, t 3.74, 694 independent blocks. By quartile of that prior return it runs from -2.94% (t -2.73) in the falling quartile to +3.39% (t 1.83) in the strongest. In flat blocks the same slope is -0.018 (t -0.74).
- **F4:** The size of the 50/200 spread does not grade the move that follows. Active blocks by raw spread quartile return +0.14%, +1.30%, -0.53% and -0.70% over 10 bars against holding, and the verdict's slope on the forecast has t 0.37. Yet the book puts its largest allocation (0.89) on the top forecast bucket.
- **F5:** The gain against holding is lost mostly while flat. On the 8454 flat days the coin earned 0.001295 a day while the book earned 0.000018, so the book's mean is 0.000400 a day against the coin's 0.001287. The weakest active bucket (forecast 0 to 5, 2154 days) earned -0.000011 a day.
- **F6:** The book's 100 worst single days come at full size after strong runs. Mean allocation was 0.99 and mean forecast 17.6, with 80% at forecast above 15 against 27% of all long days, and the mean prior 20-day return was +14.7% against +4.6% on all long days.
- **F7:** Keeping the book's daily return only on days after a rising 20-day return, and setting it to zero otherwise, lifts the pooled Sharpe from 0.36 to 0.46 but lowers the mean from 0.000400 to 0.000319. So the filter alone cures the falls rather than the low mean.

## Ideas
- `002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum` (from F1, F2, F3, F4, F7): While the 50-day SMA of the close is above the 200-day SMA, the coin keeps drifting upward, and the more so the larger its rise over the recent weeks, only while that recent-weeks return is positive.
- `002-01_sma-golden-cross-upward-drift.d2_recent-return-predicts-drift` (from F3, F5): New idea: a coin's return over the next couple of weeks is larger the larger its return over the past several weeks, whatever the position of its moving averages.
- `002-01_sma-golden-cross-upward-drift.d3_momentum-with-fading-extremes` (from F3, F6): While the 50-day SMA of the close is above the 200-day SMA, the coin keeps drifting upward, and the more so the larger its recent-weeks rise, except that the drift per unit of risk shrinks as that recent rise becomes extreme.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
