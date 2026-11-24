---
line: 7.g patterns
backtest: 031-01_wide-flat-day-ends-uprun_1d
idea tested: 031-01_wide-flat-day-ends-uprun
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5072 USD
---
## Findings
- **F1:** In folds B and C, wide flat days after a 5-day rise (range at least 1.5x the 20-day mean, flatness at least 0.9) were followed by a 5-day move in the run's direction, not against it. The move was +3.00 % above normal drift (z +0.26, t 1.69, 38 cases on 32 days). That is the opposite of the tested fall, but it cannot be told from chance after this many angles.
- **F2:** The wide range adds no graded move back. Narrow flat days after a rise (range under 0.8x) were followed by +0.76 % (t 0.67, 156 cases), and the wide flat days by +3.00 % (t 1.69), both in the run's direction.
- **F3:** Grading does not hold inside wide days. Among wide days after a rise, the slope of the 5-day z-move on range ratio has t 0.51 and on close position t 0.62 (373 cases); after a fall, t is -1.08 and -0.70 (304 cases). The widest flat days (range at least 2x) show -3.87 % in the long direction (t -1.86, 21 cases), the reverse sign of F1.
- **F4:** On the 5-day grid (1,422 to 1,638 cases), past returns barely predict the next 5 days. The slope of the 5-day z-move on past return has t 0.46 (5-day), 0.59 (10-day), 0.91 (20-day) and 0.77 (60-day); the vol-scaled 20-day return reaches only t 1.72. The 20-day-return quintiles are not monotonic (-2.76 %, t -2.88, then +2.37 %, t 2.61, in the middle quintiles). The sign of the 20-day slope also flips across windows: w7 to w9 at -1.1 to -1.2, later windows mixed.
- **F5:** Weekday 1-day returns show only Thursday (+0.61 %, t 1.94) and Friday (+0.52 %, t 2.09) near t 2 among 7 weekdays, about what chance gives for 7 tests.
- **F6:** The book is just a short on the coin. On its 489 active coin-days its daily return averaged -0.079 %, was positive on 46.8 % of them, and correlated -0.73 with the coin's own return. Net trade results spread by coin from +6.2 % (XRP, 19 trades) to -8.3 % (XMR, 9 trades) and by window from -7.5 % to +10.5 %, with no pattern by place.

## Ideas
- No ideas: I looked at the theme's situation (wide and narrow flat days after rises and falls, close position, range grade), past 5- to 60-day returns, volatility level, weekday and the book's days, and no pattern stood out from chance (largest |t| about 2.9 in a non-monotonic quintile, among more than 60 comparisons). The theme's move back after wide flat days is not in these folds: the sign is opposite (F1) and the wide range adds nothing graded (F2, F3).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
