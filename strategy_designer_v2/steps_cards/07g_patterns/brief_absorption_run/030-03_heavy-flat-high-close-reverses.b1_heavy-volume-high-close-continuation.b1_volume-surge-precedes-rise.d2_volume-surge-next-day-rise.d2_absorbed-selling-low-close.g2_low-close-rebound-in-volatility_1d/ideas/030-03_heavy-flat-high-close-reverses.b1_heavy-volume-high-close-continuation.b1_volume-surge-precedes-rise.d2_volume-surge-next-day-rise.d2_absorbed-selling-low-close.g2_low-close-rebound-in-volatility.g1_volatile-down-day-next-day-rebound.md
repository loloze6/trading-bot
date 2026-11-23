---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past day relative to its 20-day daily volatility, and the higher that volatility, the more the coin rises over the next day.
Consequence: A trader buys after large falls in volatile stretches, larger the larger the fall and the volatility, and refuses the trade after small falls or in calm stretches.
Why:
- F1: The day's own return, scaled by volatility, carries the next-day rebound better than where the close sat in the range. In a pooled regression of the next-day excess return on the close location × 20-day volatility, the day's return and the volatility, the location term falls to t 0.71 while the day's return has t −5.86. With the day's return × normalised volatility added, that term has t −5.96 and the location term drops to t 2.52.
- F2: The rebound is graded by the size of the fall and exists only in volatile stretches. In the high-volatility half, next-day excess returns run from +1.09 % (t 5.56, n 1196) after a coin's worst-decile days to −0.45 % (t −2.38, n 1212) after its best-decile days. In the low-volatility half the same deciles give +0.12 % (t 0.50) and +0.29 % (t 1.17).
- F3: The reversal holds coin by coin and year by year. The slope of the next-day excess return on the day's return is negative in all 6 coins (t −8.38 for XMR, −1.60 for XRP) and in 7 of 8 years (2020 t −7.11; 2025 t +1.63).
