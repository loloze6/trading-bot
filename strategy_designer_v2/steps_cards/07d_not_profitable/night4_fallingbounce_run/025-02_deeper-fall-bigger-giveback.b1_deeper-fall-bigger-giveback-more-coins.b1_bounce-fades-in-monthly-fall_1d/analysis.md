---
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d
idea tested: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4138 USD
---
## Findings
- **F1:** The book barely trades and so barely earns: only 227 of 36768 bars (0.6 %) were active, the book was non-zero on 305 of 2898 days, and its mean daily return is 0.004 % against 0.138 % for holding the coins, so the 0.71 % per-case edge never adds up to a daily return.
- **F2:** The fade is not limited to rises of 2 or more usual moves. On up days with both the 90-day and 30-day returns negative, the next-day drift-adjusted return is already -0.34 % (t -2.64, n 1127) for rises of 0 to 1 usual moves and -0.81 % (t -2.65, n 177) for rises of 1 to 1.5. The 2-or-more band holds only 69 bars.
- **F3:** The fade is graded by the size of the rise and shows more clearly over 3 days than over 1. On non-overlapping 3-day stretches of up days with both returns negative, the slope is -1.88 % per usual move (corr -0.155, p 0.0006, 490 cases), against -0.36 % per usual move at 1 day (corr -0.050, p 0.058). For rises of 2 to 3 usual moves, the 3-day move is -4.96 % (t -3.32, 21 cases) against -1.36 % at 1 day.
- **F4:** The depth of the 30-day fall does not grade the fade. On up days with a negative 30-day return, the next-day move by 30-day-return quartile runs -0.37 %, -0.55 %, -0.28 %, -0.24 % from deepest to shallowest, so the deepest falls are not followed by the largest givebacks.
- **F5:** A negative 90-day return is not needed. With the 90-day return positive and the 30-day negative, rises of 0 to 1 usual moves are followed by -0.34 % the next day (t -4.26, n 3754). Over 3 days, rises of 1 to 1.5 usual moves are followed by -1.90 % (t -3.98, 234 cases) and rises of 2 to 3 by -2.07 % (t -2.12, 64 cases). Across all up days with a negative 30-day return, the 3-day slope is -1.11 % per usual move (corr -0.085, p 0.0001, 2231 cases).
- **F6:** The opposite holds in rising months. On up days with a positive 30-day return, larger rises are followed by larger further rises: the 3-day slope is +1.44 % per usual move (corr +0.105, p < 0.0001, 2476 cases). With both the 90-day and 30-day returns positive, rises of 2 to 3 usual moves are followed by +0.76 % the next day (t 2.68, n 543) and +1.32 % over 3 days (t 1.94, 191 cases).
- **F7:** At 1 day, the per-case moves of the broader situations (-0.34 % to -0.81 %) are only 1.5 to 3.7 times the 0.22 % cost of a trade. At 3 days, the same situations give -1.4 % to -5.0 %, 6 to 22 times the cost.

## Ideas
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall.d1_bounce-size-grades-three-day-giveback` (from F1, F2, F3, F4, F7): In a coin whose 90-day return is negative and that has just had a one-day rise, only while its 30-day return is also negative, the larger that rise measured in its usual daily moves, the larger its fall over the next 3 days.
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall.d2_monthly-fall-bounces-fade` (from F1, F3, F5, F7): In a coin whose 30-day return is negative, the larger its one-day rise measured in its usual daily moves, the larger its fall over the next 3 days.
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall.d3_rising-month-rises-extend` (from F1, F6, F7): In a coin whose 30-day return is positive, the larger its one-day rise measured in its usual daily moves, the larger its further rise over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
