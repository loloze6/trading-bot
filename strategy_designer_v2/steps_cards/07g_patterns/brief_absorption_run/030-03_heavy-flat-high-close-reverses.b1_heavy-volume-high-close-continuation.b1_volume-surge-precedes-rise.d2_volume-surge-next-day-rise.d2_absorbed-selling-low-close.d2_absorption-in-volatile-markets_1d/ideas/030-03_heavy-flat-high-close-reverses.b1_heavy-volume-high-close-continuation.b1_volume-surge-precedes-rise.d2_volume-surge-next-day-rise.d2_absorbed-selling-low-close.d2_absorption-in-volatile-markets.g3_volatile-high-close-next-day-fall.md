---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 20-day volatility is high against its own history, the closer the day's close sits to its high, the more the coin falls over the next day.
Consequence: A trader takes the short side, or refuses a long, after volatile-regime days that close near their high.
Why:
- F1: On regime-active bars (20-day volatility at or above its 60-day mean), the next-day move beyond the coin's mean rises steadily with how low the close sits in the range: from −0.39 % (t −2.84, 1582 bars) for closes nearest the high to +0.87 % (t 6.11, 1486 bars) for closes nearest the low. On inactive bars no quintile reaches |t| 1.2. The idea's whole effect sits in its lowest-close fifth, at a per-case move about 4.5 times the 0.19 % cost of a trade.
- F3: In the highest 20-day-volatility tercile, the next-day move falls with the day's own return. The weakest-day quintile is followed by +1.05 % (t 4.01) and the second by +0.79 % (t 3.13), the middle and fourth by −0.54 % (t −2.15) and −0.65 % (t −2.79). In the lowest-volatility tercile no such ordering appears (the weakest quintile is +0.11 %, t 0.41).
