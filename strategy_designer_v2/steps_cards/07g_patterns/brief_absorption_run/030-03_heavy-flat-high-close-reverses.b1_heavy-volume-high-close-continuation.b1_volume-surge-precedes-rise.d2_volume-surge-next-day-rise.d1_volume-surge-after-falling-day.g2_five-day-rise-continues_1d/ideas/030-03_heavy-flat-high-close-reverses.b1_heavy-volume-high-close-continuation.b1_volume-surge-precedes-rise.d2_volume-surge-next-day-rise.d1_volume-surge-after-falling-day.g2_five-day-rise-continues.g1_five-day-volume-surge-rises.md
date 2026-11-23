---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's traded volume over the past 5 days, measured against its usual volume over the past 60 days, the more the coin rises over the next 3 days.
Consequence: A trader leans long a coin after a sustained surge in its 5-day volume, more so the larger the surge, and treats quiet volume as no reason to be long.
Why:
- F1: Over all the 3-day grid cases (n 3886), the coin's excess 3-day return, in usual 3-day moves, rises with the log of its 5-day volume against its 60-day average volume, slope +0.125 per log unit with t 4.49. This is the strongest pattern across about twenty angles, and stronger than the tested 5-day-rise forecast itself (slope t 2.79 on its 2850 cases).
- F3: The tested idea's gain sits on heavy volume. Among cases with a positive forecast, the top tercile of 1-day relative volume gives +0.91 % excess over 3 days (t 2.78, n 854), while the lower two terciles give −0.01 % (t −0.03) and −0.17 % (t −0.73). In the full grid, though, the rise × volume interaction term is −0.005 with t −0.42, so volume adds to the rise rather than amplifying it.
