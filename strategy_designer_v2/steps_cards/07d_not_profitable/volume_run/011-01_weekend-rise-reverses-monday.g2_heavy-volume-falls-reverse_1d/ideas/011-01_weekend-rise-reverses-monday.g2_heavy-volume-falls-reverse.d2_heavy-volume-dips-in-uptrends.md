---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's large one-day fall made on heavy volume compared with its 60-day average volume is partly undone over the next 1 day, and the heavier that day's volume, the larger the next day's rebound. While the coin's 20-day return is positive, the rebound keeps growing over the next 5 days.
Consequence: A trader should hold heavy-volume dip buys longer when they occur inside a rising month, and treat such dips as entries into the trend rather than one-day bounces.
Why:
- F5: The rebound keeps going past the one day the book holds: excess returns on active bars are 0.0087 at 1 day (t 5.61), 0.0124 at 3 days and 0.0137 at 5 days (n 1488), with day 2 adding 0.0023 (t 1.55); on a non-overlapping 3-day grid, heavy-volume down days gain 0.0259 (t 4.84, n 397).
- F6: Over longer horizons the rebound is larger after a rising month: when the coin's 20-day return was positive, active bars gain 0.0179 over 3 days and 0.0261 over 5 days (n 606), against 0.0088 and 0.0054 after a falling 20 days (n 917), though the next day alone is 0.0061 against 0.0104.
