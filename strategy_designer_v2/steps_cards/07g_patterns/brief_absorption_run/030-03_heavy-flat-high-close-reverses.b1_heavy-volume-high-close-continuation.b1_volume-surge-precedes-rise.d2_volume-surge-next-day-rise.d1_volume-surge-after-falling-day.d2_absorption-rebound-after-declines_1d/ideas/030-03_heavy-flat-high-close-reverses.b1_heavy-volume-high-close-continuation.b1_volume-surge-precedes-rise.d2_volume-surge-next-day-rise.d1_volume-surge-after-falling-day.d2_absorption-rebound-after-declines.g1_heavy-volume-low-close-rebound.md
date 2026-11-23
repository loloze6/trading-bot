---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a down day, the heavier the coin's volume relative to its own prior 20-day average and the nearer its close sits to the day's low, the more the coin rises over the next day.
Consequence: A trader weights the next-day long after a heavy-volume fall by how deep in the day's range the close settled, rather than by the size of the prior 20-day decline.
Why:
- F1: How heavy the volume was and how low the close sat in the day's range, taken together, predict the next day better than the tested forecast. The signal is the negative of the close's position in the range times the positive part of the log of volume over its prior 20-day mean. In a pooled regression on the next-day excess return that also holds the day's move, the close position, the volume, the range and the forecast, this signal has t 3.85 while the forecast falls to t 0.26 (15,796 days).
- F2: Sorted into quintiles of that signal, the top quintile (heavy volume, close near the low) earns +0.375 % next-day excess, t 3.87, over 3,159 days. Its total move is +0.50 %, which is 2.6 times the 0.19 % cost of a trade. In the two-way table, the heaviest-volume quintile with the lowest-close quintile earns +1.41 % next-day excess.
- F3: The signal of F1 holds across coins and years. Its per-coin t is positive in 5 of 6 coins (BTC 3.46, ETH 3.04, LTC 2.83, XMR 4.92, XRP 1.52; ZEC -0.26). Its per-year t is positive in 7 of 8 years (2018 3.31, 2020 4.90, 2021 2.22; 2024 -1.42).
- F4: The signal of F1 is a one-day effect. On non-overlapping 3-day returns its slope has t -0.26 (5,147 cases).
- F6: The coin's own largest falls are followed by a rebound. The decile of the largest falls, in units of the 20-day daily standard deviation, earns +0.61 % next-day excess (t 4.22, 1,580 days). The next decile earns +0.30 % (t 2.51). The seventh decile of rises earns -0.34 % (t -3.07).
