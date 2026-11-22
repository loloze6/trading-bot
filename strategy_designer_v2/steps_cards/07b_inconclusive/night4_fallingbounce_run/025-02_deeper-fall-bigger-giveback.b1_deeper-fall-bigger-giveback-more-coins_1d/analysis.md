---
line: 7.b inconclusive
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins_1d
idea tested: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4459 USD
---
## Findings
- **F1:** The tested grading does not hold, and points the wrong way at longer horizons. Across the 445 bounce cases in a falling 90-day market (one per 5-day grid cell), the slope of the excess return on the 90-day return has t -1.23 at 5 days and t -2.08 at 10 days. By quartile, the deepest 90-day falls are followed by a rise: +1.36 % excess over 5 days (t 1.05, 112 cases) and +3.87 % over 10 days (t 2.13). The second quartile falls -3.69 % over 10 days (t -2.74). This is why step 5's slope t was -0.47 and its supporting mean was -0.10 % per case.
- **F2:** The giveback shows only when the coin's 30-day return is also negative. In those 177 cases the excess return is -1.73 % the next day (t -4.03), -1.79 % over 3 days (t -2.51) and -2.60 % over 5 days (t -3.17). In the 169 cases with a positive 30-day return it is +0.36 % over 5 days (t 0.32). The 99 cases where the 30-day return could not be computed rose +2.03 % (t 1.26) and diluted the test.
- **F3:** Inside the cases with a negative 30-day return, the effect is graded on the depth of the 30-day fall. The slope of the next day's excess return on the 30-day return is 0.116 (t 3.07, 176 cases): a deeper 30-day fall comes with a larger next-day fall. The grading fades with horizon (t 1.73 at 3 days, t 0.93 at 5 days).
- **F4:** Across all 445 cases, the size of the bounce day itself grades the next day's move. The slope of the excess 1-day return on the bounce day's return is -0.148 (t -3.92, 441 cases) and still -0.222 at 5 days (t -2.29). The top bounce quartile gives back -2.10 % the next day (t -3.11, 92 cases). The grading is not monotone, because the smallest quartile also falls (-0.75 %, t -1.44).
- **F5:** The effect is mixed across years. 2022 carries the fall, with -5.15 % excess over 5 days (t -2.92, 100 cases). 2021 goes the other way (+4.40 %, t 2.59, 36 cases) and so does 2024 (+2.53 %, t 1.52, 55 cases). No coin stands out alone: the largest |t| over 5 days is 1.55, for NEAR.
- **F6:** The tested idea's measured size is too small to pay, while the next-day giveback of F2 is large enough. The unusual move per case is -0.10 % over 5 days, -0.4 times the 0.22 % cost of a trade. The next-day giveback where the 30-day return is negative is about 8 times that cost.

## Ideas
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall` (from F2, F3, F5, F6): In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, only while its 30-day return is also negative, the deeper its 30-day fall, the larger its fall over the next day.
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b2_sharper-bounce-bigger-giveback` (from F4, F1, F6): In a coin whose 90-day return is negative, the larger its one-day rise measured in its usual daily moves, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
