---
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback_1d
idea tested: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3482 USD
---
## Findings
- **F1:** In the falling regime (90-day return below 0), the next-day move runs against the day's scaled move across the whole range: the slope of next-day strength on the scaled one-day return is -0.066 (t -6.08, 7335 days), against -0.019 (t -1.65, 7885 days) outside the regime, and it is negative on all six coins (t from -1.63 to -4.28).
- **F2:** Within the falling regime the reversal is carried more by down days than by up days: on down days the slope is -0.092 (t -4.16, 3807 days), on up days only -0.031 (t -1.33, 3519 days); days with a scaled fall between 1 and 2 usual moves are followed by +0.137 usual moves the next day (t 3.65, 783 days).
- **F3:** In the falling regime the next-day rebound after a fall of more than one usual move averages +0.65 % over the coin's drift (1074 days), larger than the +0.46 % giveback after a rise of more than one usual move (884 days); both exceed the 0.19 % cost of a trade.
- **F4:** The reversal grows with the depth of the 90-day fall: the slope is -0.134 (t -3.55, 734 days) in the deepest third of 90-day returns, -0.057 (t -1.90) in the middle third and -0.037 (t -1.24) in the shallowest third.
- **F5:** The effect is one day long and uneven over the years: over two days on non-overlapping cases the falling-regime slope drops to -0.014 (t -0.95, 3614 cases), and the one-day slope is strong in 2018 (t -3.57), 2020 (t -8.63) and 2021 (t -3.43) but near zero from 2022 to 2025 (t between -0.26 and -1.42).
- **F6:** The tested bounce short barely moves the book: when a position is held the book's mean bar return is -0.008 % (t -0.34, 4524 bars), and within the falling regime the giveback after rises does not grow past 2 usual moves (-0.085 at 1-2 moves, -0.138 above 2 moves, t -2.58 and -2.08), which matches the failed top-half against bottom-half check.
- **F7:** Weekdays differ in next-day strength (Friday +0.060, t 3.74; Wednesday -0.066, t -2.92; 2478 to 2490 days each), and Thursday plus Friday beat Monday plus Wednesday in 7 of 8 years. Among the many angles examined, this pattern is not graded and stays a side observation.

## Ideas
- `025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.g1_falling-market-selloff-snaps-back` (from F1, F2, F3, F5): In a coin whose 90-day return is negative, the larger its one-day fall measured in usual daily moves, the larger its rise over the next day.
- `025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.g2_deeper-fall-sharper-reversal` (from F1, F4, F5): In a coin whose 90-day return is negative, the deeper that 90-day fall, the more the next day reverses the size of the day's move in usual daily moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
