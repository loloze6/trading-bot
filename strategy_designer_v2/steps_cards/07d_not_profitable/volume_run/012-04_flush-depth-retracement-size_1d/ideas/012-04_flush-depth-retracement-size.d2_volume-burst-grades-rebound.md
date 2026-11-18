---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.d not profitable
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among sharp daily falls, the larger the bar's volume against its prior 20-day mean, the larger the price rise over the next 3 days.
Consequence: A trader would treat the size of the volume burst on a fall as the strength of the expected rebound and refuse to buy quiet falls.
Why:
- F2: The book trades too rarely (0.0043 trades per bar) because the wick condition cuts the situation down and removes its effect: falls of at least 1.5 usual moves on at least 1.5x volume give 477 bars with excess returns of +0.0086 over 1 day (t 2.92) and +0.0082 over 3 days (t 2.16), while adding a lower wick of at least 0.3 of the range leaves 145 bars with -0.0070 over 1 day (t -1.30).
- F4: Volume carries the rebound: falls of at least 2 usual moves on at least twice the usual volume earn +0.0123 over 3 days (t 2.06, n 195), the same falls without the burst earn -0.0065 (t -1.29, n 217), and among 1.5-move falls the 3-day slope on volume ratio is positive (t 2.13).
