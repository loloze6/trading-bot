---
line: 7.b inconclusive
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3488 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar. On the 627 cases with forecast ≤ -2, the short-direction unusual move is +0.86 % over 10 days (t 1.47). The verdict's size is +0.51 % per case, a strength of 0.034, against a usual 10-day move of 14.49 %. The same signal at 5 days gives +0.52 % (t 1.88, 1,276 cases) and at 20 days +1.17 % (t 0.90, 305 cases). The effect is real in sign but too small for 627 cases to show clearly.
- **F2:** The supporting check could not be computed, because the forecast saturates. 320 of the 627 cases sit at the cap of -20, so the median |forecast| is 20 and no case is above it (0 above, 627 at or below). The test never measured whether a larger cluster gives a larger fall.
- **F3:** The cluster's raw value, before saturation, does grade the fall.
- **F4:** The effect is mixed across periods and coins.
- **F5:** The fall is larger the less the coin has already fallen over the past 20 days. Among the cases, by 20-day return quartile:
- **F6:** Over all cases the book cannot pay. The total short move per case is -0.35 % (-0.67 % in the verdict), because the coins' normal drift works against the short by -1.19 %, against a round trip of 0.19 %. The strong subsets are different:

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average.b1_broken-support-more-coins` (from F1, F3, F4): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the close is below its 50-day average.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average.b2_fresh-break-below-support` (from F3, F5, F6): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, and the larger still the less the coin has already fallen over its past 20 days, only while the close is below its 50-day average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
