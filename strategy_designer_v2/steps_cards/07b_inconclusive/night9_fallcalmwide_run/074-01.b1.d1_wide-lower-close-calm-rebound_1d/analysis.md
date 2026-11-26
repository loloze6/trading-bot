---
line: 7.b inconclusive
backtest: 074-01.b1.d1_wide-lower-close-calm-rebound_1d
idea tested: 074-01.b1.d1_wide-lower-close-calm-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3829 USD
---
## Findings
- **F1:** In the shown folds B and C the effect is clearly on the predicted side, but it is not graded by width: the 206 cases (107 days) have a mean next-day excess return of +1.63 % (day-clustered t 2.98), while across width quartiles the next-day mean is flat (+1.46 %, +1.51 %, +2.52 %, +1.29 %), width correlates 0.02 with the next-day move, and the forecast correlates -0.03.
- **F2:** What grades the rebound is how close the close sits to the day's low, not the width: the close-location measure (high − close)/(high − low) correlates 0.16 with the next-day move. A regression of the next-day excess on location and width gives +0.067 per unit of location and only +0.002 per unit of width. Cases closing in the lowest fifth of the range earn +3.50 % (t 3.61, 29 days) and +2.64 % (t 3.88, 20 days), against +0.32 % (t 0.30, 32 days) for closes just below mid-range.
- **F3:** Closeness to the low carries the effect even among the widest days: wide days with a close in the lowest quarter earn +3.15 % the next day (t 4.41, 26 days), while wide days closing nearer mid-range earn +0.87 % (t 1.03, 32 days). Narrower days closing low earn +2.23 % (t 2.54, 35 days).
- **F4:** The rebound keeps building past the plan's one-day horizon: the day-clustered mean excess is +1.63 % at 1 day (t 2.98), +2.63 % at 2 days (t 3.45), +3.47 % at 3 days (t 3.66) and +3.34 % at 5 days (t 2.75). Over 3 days, cases closing in the lowest tenth earn +5.98 % (t 3.83) and those in the 0.8–0.9 band +4.03 % (t 4.17).
- **F5:** The shown folds give a stronger result than the verdict's all-fold t of 1.71 (641 cases, 330 days), so folds A and D are weaker. The test already used every fold and all 19 coins on daily bars, so no more data exists to rerun the idea unchanged. The answer is to move the grading and the horizon to where the effect shows (F2–F4).

## Ideas
- `074-01.b1.d1.b1_wide-day-nearer-low-rebounds` (from F1, F2, F3, F5): In a rising, calm market, a day whose high-to-low range is wide against the coin's 30-day swing of daily returns and that closes in the lower part of its range is followed by a rise over the next day; the closer the close sits to the day's low, the larger the rise.
- `074-01.b1.d1.b2_low-close-three-day-rebound` (from F2, F4, F5): In a rising, calm market, a day whose high-to-low range is wide against the coin's 30-day swing of daily returns and that closes in the lower part of its range is followed by a rise over the next three days; the closer the close sits to the day's low, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
