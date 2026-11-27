---
line: 7.g patterns
backtest: 067-01.b1.g1.b1.g1.d1_deepest-choppy-slides-continue_1d
idea tested: 067-01.b1.g1.b1.g1.d1_deepest-choppy-slides-continue
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4030 USD
---
## Findings
- **F1:** In a choppy market (60-day return between -10 % and +10 %), the 30-day return measured in the coin's own 30-day swing (30-day return / (30-day daily standard deviation × √30)) ranks the next 10 days' excess return with Spearman rho 0.43 (p 0.0001, 75 non-overlapping cases), and the next 5 days' with rho 0.35 (p 0.00001, 149 cases); the plain 30-day return gives rho 0.47 at 10 days and 0.36 at 5 days.
- **F2:** The effect is graded. At 10 days, the lowest fifth of that scaled 30-day return is followed by -16.0 % excess (t -6.2, n 15) and the highest fifth by +8.3 % (t 1.4). At 5 days the quintiles run -8.8 %, -3.2 %, -2.6 %, +2.9 %, +4.3 %. Cases beyond one usual swing earn +9.5 % in the month's direction over 5 days (t 2.28, 26 cases on 17 days), against +2.5 % for the others (t 2.25, 123 cases).
- **F3:** The tested book never traded: 0 trades, 0 % of coin-days in a position, trades per day 0.000194. The regime of a 30-day fall of at least 2 usual monthly moves inside a choppy market almost never occurs, so the threshold idea was not tested, while the graded relation of F1 and F2 holds across the whole range.
- **F4:** Read in the month's direction, the choppy-market 5-day excess return is +3.7 % (day-clustered t 2.49, 149 cases on 68 days; total move +3.6 %). After falls it is +5.0 % (t 2.43, 77 cases on 42 days) and after rises +2.3 % (t 1.07, 72 cases on 36 days), so the continuation of slides is the surer side. At 10 days the result is +4.6 % with t 1.52 on only 33 days.
- **F5:** The effect is specific to the choppy band. The same scaled 30-day return has no ranking power over the next 10 days when the 60-day return is from -20 % to -10 % (rho -0.01, n 43), below -20 % (rho 0.03, n 143) or above +20 % (rho 0.05, n 143). It is weak from +10 % to +20 % (rho 0.26, p 0.11). Over 5 days, rising markets show rho 0.06 (p 0.24) and falling markets 0.08 (p 0.14).
- **F6:** Inside the choppy band, calm days carry the effect (10-day rho 0.32, p 0.02, lowest fifth -12.5 % with t -3.2, n 11). Agitated choppy days are too few to read (218 bars in all).
- **F7:** Across windows the effect is uneven: the 5-day mean in the month's direction is positive in 7 of the 12 windows, and large ones (w12 +4.9 %, w16 +31 %, w18 +12.8 %) carry most of it.
- **F8:** Other angles do not stand out after this many looks or are already held. The next-day reversal after a large daily move in falling markets (rho -0.11, p 3e-7, about 2,000 cases) is already on the map as falling agitated next-day reversal. The Friday gain of +0.41 % (t 3.05) and the Wednesday loss of -0.48 % (t -2.8) change sign across years 2018 to 2021. The close's place in the day's range does not predict the next 3 days (rho -0.01, p 0.60).

## Ideas
- `067-01.b1.g1.b1.g1.d1.g1_choppy-scaled-month-continues` (from F1, F2, F3, F5, F7): In a choppy market, a coin's 30-day return measured against its own 30-day swing points the way of its move over the next 5 days, in both directions, and the larger the month's move in usual swings, the larger the move that follows.
- `067-01.b1.g1.b1.g1.d1.g2_calm-choppy-slides-keep-falling` (from F2, F3, F4, F6): In a choppy, calm market, a coin's fall over the past 30 days, measured against its own 30-day swing, is followed by a further fall over the next 5 days, and the deeper the fall in usual swings, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
