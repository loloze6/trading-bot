---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: New idea: a coin's return over the next couple of weeks is larger the larger its return over the past several weeks, whatever the position of its moving averages.
Consequence: A trader would grade long exposure by the coin's own recent-weeks return in every state, which recovers the rising moves the cross-gated book misses while flat.
Why:
- F3: When the forecast is positive, the next 10 bars' return above holding rises with the coin's prior 20-bar return: slope 0.103, t 3.74, 694 independent blocks. By quartile of that prior return it runs from -2.94% (t -2.73) in the falling quartile to +3.39% (t 1.83) in the strongest. In flat blocks the same slope is -0.018 (t -0.74).
- F5: The gain against holding is lost mostly while flat. On the 8454 flat days the coin earned 0.001295 a day while the book earned 0.000018, so the book's mean is 0.000400 a day against the coin's 0.001287. The weakest active bucket (forecast 0 to 5, 2154 days) earned -0.000011 a day.
