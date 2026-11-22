---
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation_1d
idea tested: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4054 USD
---
## Findings
- **F1:** The tested effect sits entirely in 2018-2021 and turns over after that. The forecast's slope on the drift-removed 5-day move is positive in every year from 2018 to 2021 (t 1.25, 2.36, 2.65, 2.79, about 426 cases a year) and negative in every year from 2022 to 2025 (t −0.94, −0.83, −1.47, −0.91). The book follows the same split: its mean daily return is +0.096 %, +0.020 %, +0.159 % and +0.112 % in 2018-2021, then −0.058 %, −0.040 %, −0.064 % and −0.053 % in 2022-2025.
- **F2:** The book's gain comes from its long side. 3810 long trades earned +3.56 % each after fees, while 4832 short trades lost −0.60 % each. On the grid, the top fifth of range position (mean 0.97 of the 30-day range) is followed by +1.39 % above drift over 5 days (t 2.36, 511 cases), while the bottom fifth (mean 0.05) is followed by only −0.37 % (t −0.63).
- **F3:** Flatness does not scale the move as the idea says. The least flat fifth of 30-day windows, the one-way months, is followed by +1.52 % above drift (t 2.78, 511 cases), which is the largest of the five fifths. The flattest fifth is followed by −0.47 % (t −1.13). By 30-day net move against the range, the top fifth is followed by +1.06 % (t 1.88) and the second-lowest fifth by −1.32 % (t −3.13), which reads as continuation of the month's trend.
- **F4:** The continuation is strongest when the coin is calm. The slope of the 5-day move on position in range is 0.186 (t 3.90, 756 cases) when 10-day volatility is low against 60-day volatility, and −0.040 (t −0.77) in the middle third. When 20-day volatility is low against the window's own level, the slope of the 5-day move on the 30-day net move is 0.281 (t 4.78), against −0.086 (t −1.74) when volatility is high. However, a graded interaction of position with calm is not reliable (t 1.03), and in 2022-2025 the slope is near zero or negative at every volatility level (t −0.02, −1.53, −1.26).
- **F5:** Saturday stands out as a pattern of its own. Coin returns on Saturdays average +0.454 % a day against much smaller means on other days (t 5.53, 2484 coin-days). The gap holds in both 2018-2021 (t 3.43) and 2022-2025 (t 2.53), and in five of six coins (t 1.59 to 2.67; BTC 0.34). The book's best weekday is also Saturday, at +0.119 % a day. This is a fixed calendar condition, not a graded situation, so no idea is written from it.

## Ideas
- `023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.g1_upside-range-breakout-continuation` (from F2, F3): The closer a coin's close sits to the top of its 30-day closing range, the larger its rise over the next 5 days; a close near the bottom of the range is followed by little further fall.
- `023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.g2_calm-trend-month-continuation` (from F3, F4, F1): The larger a coin's 30-day net move against its 30-day closing range, the larger its move in that same direction over the next 5 days, and the lower its 10-day volatility against its 60-day volatility, the larger that continuation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
