---
line: 7.g patterns
backtest: 031-01.g1.g1_midweek-run-carries-into-saturday_1d
idea tested: 031-01.g1.g1_midweek-run-carries-into-saturday
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5931 USD
---
## Findings
- **F1:** At Friday's close, a longer lookback grades Saturday's excess return better than the tested Monday-to-Thursday return, and Friday's own move grades it not at all. The mean of clipped z × Saturday excess, with t from cases of one date summed over about 345 Fridays, was:
- **F2:** The 14-day signal on Fridays also grades the excess return over Saturday plus Sunday (2 days): 0.0187 with t 3.27 (345 dates). The 3-day lagged signal does not, at t 1.36, and the 5-day signal does not either, at t 1.62.
- **F3:** The 14-day grading appears only when the following day is Saturday.
- **F4:** The weekend move in the signal's direction grows with the size of the Friday 14-day return. Signed weekend excess return by quartile of |14-day z|:
- **F5:** Over 5-day returns, the Friday grading into Saturday is monotone across quintiles: Saturday excess runs −0.58 %, −0.30 %, +0.34 %, +0.79 %, +0.98 % (bottom t −1.49, top t 2.66).
- **F6:** The weekend effect of the 14-day signal holds across coins and years.
- **F7:** The 14-day weekend grading is about twice as strong when the coin's 20-day volatility is in its top tercile relative to its own median.
- **F8:** The book's results are made entirely on Saturdays, and Fridays only cost fees.

## Ideas
- `031-01.g1.g1.g1_two-week-run-carries-weekend` (from F1, F2, F3, F4, F6): The higher a coin's 14-day return, measured in its usual daily moves at Friday's close (UTC), the more it rises over the following Saturday and Sunday together.
- `031-01.g1.g1.g2_volatile-weekends-follow-trend` (from F7, F4, F2): When a coin's 20-day volatility is high relative to its usual level, its 14-day return at Friday's close (UTC) grades its move over the following Saturday and Sunday more steeply, and the larger that return, the larger the weekend move in its direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
