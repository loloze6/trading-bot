---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3879 USD
---
## Findings
- **F1:** On regime-active bars (20-day volatility at or above its 60-day mean), the next-day move beyond the coin's mean rises steadily with how low the close sits in the range: from −0.39 % (t −2.84, 1582 bars) for closes nearest the high to +0.87 % (t 6.11, 1486 bars) for closes nearest the low. On inactive bars no quintile reaches |t| 1.2. The idea's whole effect sits in its lowest-close fifth, at a per-case move about 4.5 times the 0.19 % cost of a trade.
- **F2:** The low-close effect needs the day itself to be large. In the lowest-close quintile, the next-day t is 6.28 when the day's range is in the widest tercile against its prior 20-day average, against −0.06 and −1.59 for the other terciles. It is 5.24 in the heaviest-volume tercile against 0.62 and −0.34, and 5.40 in the largest open-to-close tercile against −0.23 and −0.47.
- **F3:** In the highest 20-day-volatility tercile, the next-day move falls with the day's own return. The weakest-day quintile is followed by +1.05 % (t 4.01) and the second by +0.79 % (t 3.13), the middle and fourth by −0.54 % (t −2.15) and −0.65 % (t −2.79). In the lowest-volatility tercile no such ordering appears (the weakest quintile is +0.11 %, t 0.41).
- **F4:** Inside the book's positions, the gain sits only in the largest forecasts. The top forecast bin earns +0.45 % next day (t 4.10, 3008 bars), while the three lower bins lose −0.28 %, −0.16 % and −0.29 % (t −2.10, −1.18, −2.13, about 1500 bars each). The book's best decile of days (+2.71 %) follows a coin day of −2.33 % on average, and its worst decile (−2.40 %) comes on coin days of −5.53 %.
- **F5:** On inactive (calmer) bars, a close nearest the low is followed over the next 3 days by −0.88 % beyond the coin's mean (t −2.78, 642 non-overlapping cases). Closes in the second-highest fifth are followed by +0.69 % (t 2.29). This is the opposite of the reversal seen in the volatile regime, though it is modest given how many angles were looked at.
- **F6:** Weekdays differ: Friday's next-day move is +0.30 % (t 3.76) and Wednesday's −0.30 % (t −2.70), across about 2480 bars each. Weekday is not a graded situation, so this finding supports no idea here.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g1_wide-range-low-close-rebound` (from F2, F1, F4): The wider a coin's day range against its own prior 20-day average range, the more the coin rises over the next day, the lower the day's close sits within that range.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g2_volatile-regime-one-day-reversal` (from F3, F4): While a coin's 20-day volatility is high against its own history, the larger the coin's fall over a day, the more it rises over the next day, and the larger that volatility, the larger the rebound.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g3_volatile-high-close-next-day-fall` (from F1, F3): While a coin's 20-day volatility is high against its own history, the closer the day's close sits to its high, the more the coin falls over the next day.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g4_calm-regime-low-close-continuation` (from F5): While a coin's 20-day volatility is low against its own history, the lower the day's close sits within its high-low range, the more the coin falls over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
