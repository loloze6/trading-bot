---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On an up day, the heavier the coin's volume relative to its own prior 20-day average and the nearer its close sits to the day's low, the more the coin falls over the next day.
Consequence: A trader refuses, or reverses, a next-day long after a rally that gave back most of its range on heavy volume.
Why:
- F5: On up days only, the same signal (close low in the range, heavy volume) predicts a fall the next day. The quintiles step down: +0.13 %, -0.16 %, -0.16 %, -0.27 %, -0.37 % (top quintile t -2.85, 1,604 days each). On up days a wider range relative to the usual daily move also predicts a lower next day (t -3.32), and a larger rise predicts a higher one (t +2.93).
- F1: How heavy the volume was and how low the close sat in the day's range, taken together, predict the next day better than the tested forecast. The signal is the negative of the close's position in the range times the positive part of the log of volume over its prior 20-day mean. In a pooled regression on the next-day excess return that also holds the day's move, the close position, the volume, the range and the forecast, this signal has t 3.85 while the forecast falls to t 0.26 (15,796 days).
