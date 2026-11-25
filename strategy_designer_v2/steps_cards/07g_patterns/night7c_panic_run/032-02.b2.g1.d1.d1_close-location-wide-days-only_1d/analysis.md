---
line: 7.g patterns
backtest: 032-02.b2.g1.d1.d1_close-location-wide-days-only_1d
idea tested: 032-02.b2.g1.d1.d1_close-location-wide-days-only
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4396 USD
---
## Findings
- **F1:** On days wider than the coin's previous 20-day average range, the rebound sits only on the low-close side. After a close in the lower half of the range, the next-day excess return in the direction of the reversal is +0.88 % (t 2.94, 1245 cases). After a close in the upper half it is +0.20 % (t 0.83, 1405 cases). The book's trades show the same split: LONG trades average +0.65 % net (1433 trades) and SHORT trades −1.04 % net (1625 trades).
- **F2:** On wide days the low-close rebound is graded by how low the close sits. The next-day excess return is +1.28 % (t 2.84, 465 cases) for closes in the bottom fifth of the range (location below −0.6) and +0.41 % (t 1.09, 565 cases) for location between −0.6 and −0.2. That top bin alone is 6.7 times the 0.19 % cost of a trade, against 1.7 times for the tested idea's average case.
- **F3:** Wide days reverse only in coins that are already volatile. In the lowest tercile of 20-day return volatility the reversal is −0.15 % (t −0.42, 337 cases) in a falling month and −0.22 % (t −0.83, 606 cases) in a rising month. In the middle and top terciles it is +1.30 % (t 3.45, 335) and +1.44 % (t 2.30, 336) in a falling month, and +0.55 % (t 2.28, 552) and +0.70 % (t 1.67, 485) in a rising month.
- **F4:** The reversal follows the day's range multiple continuously rather than switching on at 1.0. By range-multiple quintile, the reversal is −0.11 % (t −0.60) and +0.00 % (t 0.02) in the two lowest quintiles (median multiple 0.43 and 0.62). It is +0.56 % (t 3.45, median 0.82), +0.49 % (t 2.16, median 1.10) and +0.60 % (t 2.57, median 1.74) in the upper three, about 1450 cases each.
- **F5:** A down day that is large relative to the coin's own volatility is followed by a rise. The lowest quintile of the day's return over its 20-day standard deviation (median −1.15) has a next-day excess return of +0.70 % (t 2.38, 1452 cases). The middle quintile shows −0.14 % (t −0.73) and the top quintile −0.11 % (t −0.47).
- **F6:** The low-close rebound lasts only one to two days. On non-overlapping grids it is +0.90 % over 1 day (t 2.01, 606 cases) and +1.38 % over 2 days (t 1.68, 340) in a falling month, then −0.42 % over 3 days (t −0.38, 178). On all wide days the reversal over 3 days is +0.01 % (t 0.02, 854).
- **F7:** The brief's own situation, a new 20-day low in a high-volatility falling month, is followed by +1.27 % over 1 day (t 1.15, 232 cases). That cannot be told from 0. A low close on a day that is not wide in a falling month is followed by −0.18 % (t −0.69, 1294), so it is the wide low close, not the new low, that carries the rebound.

## Ideas
- `032-02.b2.g1.d1.d1.g1_wide-day-low-close-rebound` (from F1, F2, F6, F7): On a day whose high-low range is wider than the coin's average daily range over the previous 20 days, the lower the close sits in the lower half of that day's range, the more the coin rises over the next 1 day.
- `032-02.b2.g1.d1.d1.g2_volatility-scaled-wide-day-reversal` (from F3, F4): After a day wider than the coin's average daily range over the previous 20 days, the higher the coin's volatility of daily returns over the past 20 days, the more its next 1-day move goes against the side of the range where the day closed.
- `032-02.b2.g1.d1.d1.g3_volatility-scaled-down-day-rebound` (from F5, F1): The further a coin's daily return falls below zero, measured in units of its standard deviation of daily returns over the past 20 days, the more the coin rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
