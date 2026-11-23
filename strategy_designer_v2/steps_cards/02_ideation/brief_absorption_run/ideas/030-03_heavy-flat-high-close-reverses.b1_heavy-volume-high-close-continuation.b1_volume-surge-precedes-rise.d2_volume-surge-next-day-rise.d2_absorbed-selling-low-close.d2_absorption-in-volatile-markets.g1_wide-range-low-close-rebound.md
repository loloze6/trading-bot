---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The wider a coin's day range against its own prior 20-day average range, the more the coin rises over the next day, the lower the day's close sits within that range.
Consequence: A trader buys only low closes on unusually wide days, where the move per case is several times the cost of a trade, and refuses low closes on ordinary-range days.
Why:
- F2: The low-close effect needs the day itself to be large. In the lowest-close quintile, the next-day t is 6.28 when the day's range is in the widest tercile against its prior 20-day average, against −0.06 and −1.59 for the other terciles. It is 5.24 in the heaviest-volume tercile against 0.62 and −0.34, and 5.40 in the largest open-to-close tercile against −0.23 and −0.47.
- F1: On regime-active bars (20-day volatility at or above its 60-day mean), the next-day move beyond the coin's mean rises steadily with how low the close sits in the range: from −0.39 % (t −2.84, 1582 bars) for closes nearest the high to +0.87 % (t 6.11, 1486 bars) for closes nearest the low. On inactive bars no quintile reaches |t| 1.2. The idea's whole effect sits in its lowest-close fifth, at a per-case move about 4.5 times the 0.19 % cost of a trade.
- F4: Inside the book's positions, the gain sits only in the largest forecasts. The top forecast bin earns +0.45 % next day (t 4.10, 3008 bars), while the three lower bins lose −0.28 %, −0.16 % and −0.29 % (t −2.10, −1.18, −2.13, about 1500 bars each). The book's best decile of days (+2.71 %) follows a coin day of −2.33 % on average, and its worst decile (−2.40 %) comes on coin days of −5.53 %.
