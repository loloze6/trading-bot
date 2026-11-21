---
line: 7.b inconclusive
backtest: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h
idea tested: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3394 USD
---
## Findings
- **F1:** The tested move shows up at 10 days and nowhere else. Over 1,093 cases the unusual move is +1.04 % at 240 hours (t 2.03). It is +0.12 % at 24 hours (t 0.81), +0.46 % at 72 hours (t 1.64) and +0.96 % at 480 hours (t 1.09). So the main measure clears t 2 by only a hair.
- **F2:** The grading the idea names fails because it runs the wrong way on the drop. Across cases, the slope of the 10-day move (in usual moves) on the depth of the 24-hour fall is −0.117 (t −2.32, n 1,009): the deepest quarter of drops is followed by −0.70 % (t −0.70, n 251), while the shallower three quarters give +0.94 % to +1.91 %. The slope on the forecast is −0.004 (t −0.84, n 1,093).
- **F3:** The 30-day prior rise is the part that is graded the predicted way. Across cases its slope is +0.22 (t 2.01, n 815), and +0.27 (t 2.35, n 678) among cases whose fall is under one usual daily move. Among drops deeper than one usual daily move it is −0.17 (t −0.55, n 137).
- **F4:** The drop adds nothing on top of the prior rise; it subtracts. On the plain 240-hour grid with a positive 30-day return:
- **F5:** The effect is a market-period effect more than a per-case one.
- **F6:** Size is not the obstacle. The unusual move is +1.08 % per case, 5.6 times the 0.19 % cost of a round trip, and the total move is 12.6 times that cost. What leaves the result unclear is the mis-signed drop grading (F2), not too few cases or too small a move.

## Ideas
- `018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge.b1_shallow-dip-after-monthly-rise` (from F2, F3, F6): When a coin's 24-hour return, read at an hourly close, falls, the coin rises over the next 10 days more than its normal drift, and the shallower the fall measured in its 30-day average absolute daily return and the larger its 30-day return before the fall, the larger the rise.
- `018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge.b2_thirty-day-rise-continues-ten-days` (from F3, F4, F5): The larger a coin's 30-day return, read at an hourly close, the more the coin rises over the next 10 days than its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
