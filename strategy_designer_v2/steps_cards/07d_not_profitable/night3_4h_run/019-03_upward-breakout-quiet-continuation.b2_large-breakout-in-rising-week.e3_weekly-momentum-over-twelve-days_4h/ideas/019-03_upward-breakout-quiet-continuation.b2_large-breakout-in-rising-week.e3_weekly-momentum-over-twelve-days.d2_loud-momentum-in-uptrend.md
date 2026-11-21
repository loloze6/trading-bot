---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next twelve days, only while its 30-day return is positive, and the more so the higher its 3-day volatility of 4h returns stands above its 30-day volatility.
Consequence: A trader would size weekly-momentum longs in a rising month larger when the coin's recent 4h bars are unusually wide.
Why:
- F4: The book's gain sits in longs taken while the coin's 30-day return is positive: their bar gains sum to +13.35 (mean +0.046 % per bar, 29,013 bars), against -0.66 for longs against the 30-day trend and -5.03 for shorts against it; long grid cases with a positive 30-day return move +3.42 % over 72 bars (t 3.06, 321 cases).
- F5: Within longs in a rising 30-day trend, the gain grows with recent volatility against its 30-day level: the mean bar gain is +0.003 % in its quietest third, +0.017 % in the middle third and +0.109 % in the loudest third (about 10,000 bars each); on the grid, quiet-ratio cases move -0.27 % (t -0.28, 324 cases) and loud ones +2.26 % (t 1.96, 324 cases), the opposite of the brief's quiet-range premise.
- F3: The long side's gain is graded by the forecast's size: long grid cases by quartile of |forecast| move -0.89 %, +3.20 %, +3.13 % and +5.13 % over 72 bars, while short quartiles move -1.27 %, -3.73 %, +0.10 % and +1.18 % in their direction, so no grade holds there.
