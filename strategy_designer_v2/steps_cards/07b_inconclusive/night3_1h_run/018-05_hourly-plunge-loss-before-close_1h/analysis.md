---
line: 7.b inconclusive
backtest: 018-05_hourly-plunge-loss-before-close_1h
idea tested: 018-05_hourly-plunge-loss-before-close
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3434 USD
---
## Findings
- **F1:** Overall, the plunge has no follow-through to the day's close, and the slight lean is the wrong way. The mean excess short return from the first -2 crossing to the UTC day's close is -2.0 bp (t -0.47, 7593 cases). At other horizons it stays near zero: -2.2 bp at 4 hours (t -0.88), -1.0 bp at 24 hours (t -0.17), +7 bp at 72 hours (t 0.68).
- **F2:** The near-zero mean hides a split by the coin's 30-day return before the plunge.
- **F3:** The rebound after a 30-day rise grows with the size of that rise, but only in the upper part. On 72-hour non-overlapping cases by quintile of the 30-day return, the excess short return is -1, +50, +56, -69 (t -2.07) and -110 bp (t -2.35). Across all cases the rank correlation is only -0.02, so the grading shows only among rising coins.
- **F4:** The rebound after a 30-day rise holds across coins and years.
- **F5:** The only real follow-through is in 2018, where it offsets the other years. There the plunge kept falling: +45 bp to the close (t 3.14) and +270 bp over 72 hours (t 8.6). Most later years lean toward a rebound, from -2 to -21 bp to the close, which is why the pooled t is near zero.
- **F6:** Plunges that first hold late in the UTC day (18 to 23 h) rebound to the close by 18 bp (t -4.06, 1352 cases) and by 46 bp over 24 hours (t -3.36). The move to the close, 18 bp, is just under the 19 bp cost of a round trip, so this does not pay at that horizon (F2 of the run findings).
- **F7:** The size of the rebound after a 30-day rise is large next to the cost. About 1.3 % over 72 hours is roughly 6.8 times the 0.19 % round trip. This fits F10 and F11 of the run findings: multi-day horizons let a move of usual strength cover the cost.

## Ideas
- `018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds` (from F2, F3, F4, F7): When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the downside while its own 30-day return is positive, the price rises over the next 3 days. The larger the 30-day rise before the plunge, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
