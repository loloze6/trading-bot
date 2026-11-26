---
line: 7.b inconclusive
backtest: 074-01.b1.b1_falling-wide-up-day-high-close-fade_1d
idea tested: 074-01.b1.b1_falling-wide-up-day-high-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4220 USD
---
## Findings
- **F1:** In folds B and C, the tested cases fall next day by only a little and unclearly: mean short-direction excess next-day return +0.56 % (t 0.99, 229 cases on 135 days), against the full test's +0.63 % (t 1.37, 341 days). The full test already used every fold and every coin that has data, so there is no more data to add.
- **F2:** The fade sits in the widest days only: below the median range multiple of 1.86 the mean is −0.00 % (t −0.00, 98 cases, 71 days), above it +1.81 % (t 2.60, 98 cases, 60 days); upper minus lower is +1.81 % (Welch t 1.82).
- **F3:** The top width quintile (range 2.3 to 7.9 times the 20-day mean) carries most of it, +2.89 % (t 2.74, 39 cases, 29 days), against −0.08 % to +0.97 % in the four lower quintiles. The width quartiles rise to +1.36 % and +2.32 % (t 2.41) in the top two.
- **F4:** Close location, the grade the tested idea added, does not sort the fade. Close-location quartiles give −0.61 %, +1.31 %, +1.01 %, +0.54 %, with Spearman 0.04. The |forecast| quartiles are not monotone either (−0.47 %, +1.68 %, +1.38 %, −0.35 %), so the plan's forecast mixes a working grade (width) with a non-working one (close location).
- **F5:** The wide-day fade is stronger when the coin is swinging more than usual:
- **F6:** The effect is spent in one day, as the brief says: the excess return is +0.56 % at 1 day, −0.31 % at 2 days (t −0.43) and +0.25 % at 3 days.
- **F7:** The fade is uneven across coins and years, which drowns the mean:

## Ideas
- `074-01.b1.b1.b1_falling-widest-up-day-fade` (from F2, F3, F4, F6): In a falling market, an up day whose high-to-low range is wide compared with the coin's average daily range over the past 20 days is followed by a fall over the next day, the wider that day's range against its 20-day average, the larger the next day's fall.
- `074-01.b1.b1.b2_agitated-downtrend-wide-day-fade` (from F2, F3, F5, F6): In a falling, agitated market, an up day whose high-to-low range is wide compared with the coin's average daily range over the past 20 days is followed by a fall over the next day, the wider that day's range against its 20-day average, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
