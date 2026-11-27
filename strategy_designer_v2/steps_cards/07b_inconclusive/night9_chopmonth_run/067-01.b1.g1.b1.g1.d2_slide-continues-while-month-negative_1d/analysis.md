---
line: 7.b inconclusive
backtest: 067-01.b1.g1.b1.g1.d2_slide-continues-while-month-negative_1d
idea tested: 067-01.b1.g1.b1.g1.d2_slide-continues-while-month-negative
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3743 USD
---
## Findings
- **F1:** The test graded the short by the 30-day return standardised over its own last 60 values, and that forecast correlates only 0.54 with the plain 30-day percent fall on the 10-day grid in the chop regime. On the folds shown, the plain fall predicts the next 10 days' excess return with slope t 5.40 (83 cases), while the standardised forecast has t 1.57 (106 cases). The effect is there, but the test read it through a distorted grade, which is why its t stopped at 1.83.
- **F2:** On the plain fall the grading is monotonic over the next 10 days, by quartile. The deepest quartile (mean 30-day return -28.1 %) has an excess return of -14.0 %, then -10.9 % (at -18.3 %), then -0.5 % (at -9.5 %), and the shallowest (at -2.7 %) has +4.4 %. Under the standardised forecast the quartiles are not ordered: -3.7 %, -9.1 %, -2.9 %, +2.1 %.
- **F3:** The plain-fall slope holds at every horizon in the chop regime: t 3.83 over 5 days (160 cases), 5.40 over 10 days (83 cases) and 3.18 over 20 days (30 cases). The standardised forecast gives t 0.41, 1.57 and 0.39 at the same horizons.
- **F4:** The plain-fall slope over 10 days is positive in calm and agitated months alike, with t 4.39 (52 cases) and t 2.83 (31 cases). It is positive in the core six coins (t 4.27, 58 cases) and in the other coins (t 3.35, 25 cases). It is positive in all four years: t 1.75, 1.65, 4.19 and 0.88 in 2018 to 2021. So it is not confined to one agitation, coin group or period.
- **F5:** The result is on the predicted side: slope t 1.83 with a mean excess of -0.79 % over 423 cases, and a size t of 2.08. The test already used every fold and coin available, so no more data exists, and the clearer answer is the idea graded by the plain depth of the fall.
- **F6:** Even graded plainly, the gain on the shallowest falls is weak. Their mean excess return is +4.4 % against the short. The 10-day mean excess across the whole short regime is -5.3 % (t -3.15, 83 cases), so the move is carried by the deeper falls.

## Ideas
- `067-01.b1.g1.b1.g1.d2.b1_plain-monthly-fall-depth-continues` (from F1, F2, F3, F4, F5, F6): In a choppy market, a coin's fall over the past 30 days is followed by a further fall over the next 10 days, only while its 30-day return is still negative. The more percent of its price the coin has lost over those 30 days, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
