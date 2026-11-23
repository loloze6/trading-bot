---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4072 USD
---
## Findings
- **F1:** The day's own return, scaled by volatility, carries the next-day rebound better than where the close sat in the range. In a pooled regression of the next-day excess return on the close location × 20-day volatility, the day's return and the volatility, the location term falls to t 0.71 while the day's return has t −5.86. With the day's return × normalised volatility added, that term has t −5.96 and the location term drops to t 2.52.
- **F2:** The rebound is graded by the size of the fall and exists only in volatile stretches. In the high-volatility half, next-day excess returns run from +1.09 % (t 5.56, n 1196) after a coin's worst-decile days to −0.45 % (t −2.38, n 1212) after its best-decile days. In the low-volatility half the same deciles give +0.12 % (t 0.50) and +0.29 % (t 1.17).
- **F3:** The reversal holds coin by coin and year by year. The slope of the next-day excess return on the day's return is negative in all 6 coins (t −8.38 for XMR, −1.60 for XRP) and in 7 of 8 years (2020 t −7.11; 2025 t +1.63).
- **F4:** Days of heavy volume relative to the coin's 20-day average are followed by a rise. In the top quarter of relative volume the next-day excess return is +0.329 % (t 3.57, n 4031), against −0.10 % to −0.12 % in the other three quarters. Log relative volume has t 5.07 controlling for the day's return and the location term, and t 2.59 on 5147 non-overlapping 3-day cases. The top quintile beats the rest in 71 % of the 24 windows.
- **F5:** The heavy-volume rise sits on up days, and its link is weaker per coin and per year. Top-quintile relative volume on up days is followed by +0.772 % (t 5.11, n 1546), while on down days it is followed by −0.031 % (t −0.22). Per coin the relative-volume slope reaches t ≥ 2 only in ZEC (3.24) and XRP (2.42), with t 0.55 to 1.74 elsewhere. By year it ranges from t 0.10 (2022) to 3.57 (2021).
- **F6:** The book's best and worst days are the coin's large moves taken at about two thirds of size. The book's top decile of days averages +4.84 % against the coins' +7.31 %, and its bottom decile −4.45 % against −6.87 %. Its gain and its falls therefore come with the market's move, which fits a Calmar of 0.46 for a book in a position on 100 % of days.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility.g1_volatile-down-day-next-day-rebound` (from F1, F2, F3): The larger a coin's fall over the past day relative to its 20-day daily volatility, and the higher that volatility, the more the coin rises over the next day.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility.g2_heavy-volume-up-day-continuation` (from F4, F5): The heavier a coin's volume over the past day relative to its average daily volume over the past 20 days, on a day it closed higher, the more it rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
