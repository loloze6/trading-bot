---
line: 7.g patterns
backtest: 041-01.b1_rising-agitated-rise-continues_1d
idea tested: 041-01.b1_rising-agitated-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3352 USD
---
## Findings
- **F1:** Inside the rising agitated profile, the next-day return does not grow with the day's scaled rise. The slope t of the excess next-day return on the day's return over its 30-day swing is 0.66 (470 non-overlapping cases). At 2, 3 and 5 days the t's are -0.39, 0.18 and 1.95 (228, 153 and 91 cases).
- **F2:** Grouped by the size of the scaled day's move, the next-day returns in the profile form no ordered pattern. Days of 0 to 1 swings up are followed by -0.65 % (t -1.44, 177 cases), days of 1 to 2 by +0.76 % (t 0.56, 43) and days above 2 by +1.08 % (t 0.61, 18). No group reaches |t| 2.
- **F3:** For the short side, the profile's average excess is negative but cannot be told from 0. It is -0.21 % over 1 day (470 cases) and -0.61 % over 3 days (153 cases). By coin it splits: ZEC -0.57 % a day (t -1.39, 356 cases), BCH +0.28 % (t 0.49, 223) and DOGE +0.16 % (t 0.09, 45).
- **F4:** None of the other situations tested shows a graded short-side effect. The tests were:
- **F5:** The weekday makes no difference to the next-day return in the profile. The most extreme day is Wednesday, at -1.06 % (t -1.25, 94 cases).
- **F6:** The book has no edge to explain. On its 457 active coin-days the mean daily return is -0.02 % (t -0.16), and only 25 % of those days are positive. The idea's total move per case is +0.23 %, 0.6 times the 0.37 % cost of a trade.

## Ideas
- No ideas: Inside the rising agitated profile, none of the angles examined shows a graded effect that stands out from chance on the short side. The angles were the day's scaled move, multi-day stretch, close location, range, wicks, volume, distance to recent highs, weekday and the book's own days. The largest t is 2.26 among about 50 tests, its sign is wrong for a short, and the profile's negative drift cannot be told from 0 (ZEC t -1.39).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
