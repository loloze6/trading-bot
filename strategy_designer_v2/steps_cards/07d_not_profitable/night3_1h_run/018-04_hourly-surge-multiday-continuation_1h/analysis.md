---
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation_1h
idea tested: 018-04_hourly-surge-multiday-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3570 USD
---
## Findings
- **F1:** The book fails on its falls, not on its gain: chained over the windows its deepest fall is 61.5 % against a yearly return of 33.1 % (Calmar 0.54 against 0.75 required), even though its Sharpe of 0.79 beats holding's by 0.24.
- **F2:** The book is in effect a scaled holding of the coins. It holds a position on 98.3 % of coin-days, at a mean allocation of 0.81 when in. Its losing windows match the coins' losing windows: in w2 the book's daily returns sum to -0.39 against the coins' -0.46, in w7 -0.33 against -0.58, and in w14 -0.49 against -0.52. Its chained fall reaches -0.54 in w2, -0.61 in w3 and -0.59 in w4, which is one long fall shared with the coins.
- **F3:** The idea has no edge of its own to offset those falls. Over the 3205 cases the unusual 120-bar move is -0.01 % (t -0.06). The total move is +0.63 %, 3.3 times the 0.19 % round trip, but it is all the coin's normal drift. The unusual move is -0.1 times the cost.
- **F4:** The size of the surge does not grade the move that follows. Across quintiles of the 24-hour return in multiples of its 30-day mean absolute value, the mean unusual move is -0.85 % (t -2.39), +0.63 %, -0.39 %, +0.25 % and +0.20 % (t 0.43), with about 592 cases each. Only the lowest quintile differs from zero, and it is negative.
- **F5:** Nearness to the 30-day high is the situation that separates the surges, though the grading is not smooth across its quintiles:
- **F6:** Surges that come after a deep fall of the previous 7 days do worse. When the 7-day return ending a day before the case is in its lowest quintile (-61 % to -12 %), the unusual 5-day move is -0.93 % (t -1.86, 583 cases), against +0.51 % (t 0.97) in the top quintile.
- **F7:** On the book's own days, nearness to the 30-day high at the previous day's close comes with more gain but not with fewer large losses:
- **F8:** A strong 30-day rise mildly helps the cases but also comes with the book's large losses:

## Ideas
- `018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high` (from F1, F2, F3, F5, F7): When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while the close stands near its 30-day high: the closer the close to its 30-day high at that hour, the larger the rise.
- `018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades` (from F4, F6): When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside after its 7-day return before that day was a fall, the price rises less than the coin's usual 5-day return over the next 5 days; the deeper that 7-day fall, the larger the shortfall.
- `018-04_hourly-surge-multiday-continuation.d3_nearness-to-monthly-high` (from F2, F5, F7): The closer a coin's hourly close stands to its 30-day high, the more the coin rises over the next 5 days compared with its usual 5-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
