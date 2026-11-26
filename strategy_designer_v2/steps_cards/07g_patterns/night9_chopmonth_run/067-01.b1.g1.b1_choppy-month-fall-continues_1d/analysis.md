---
line: 7.g patterns
backtest: 067-01.b1.g1.b1_choppy-month-fall-continues_1d
idea tested: 067-01.b1.g1.b1_choppy-month-fall-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4651 USD
---
## Findings
- **F1:** In choppy bars (folds B, C, one case per non-overlapping 10-day grid cell), the coins in the lowest fifth of 30-day returns fell 12.8 % more than their normal 10-day drift. Their mean 30-day return was -25.3 %, and the excess fall has a day-clustered t of -4.22 (32 cases on 18 days). The next fifth (mean 30-day return -11.6 %) showed only -4.4 % (t -1.52, 23 days), and the middle fifth showed +2.9 % (t 0.75). The continuation is concentrated in the deepest falls and grows faster than the fall itself.
- **F2:** Across all choppy cases, the 30-day return ranks with the next 10 days' excess move with a Spearman rho of 0.378 (p 1e-6, 157 cases). Scaling the 30-day return by the coin's own 30-day swing weakens this to rho 0.332. The raw depth of the month's move carries the information better than its depth against volatility.
- **F3:** The mirror side is weaker in these folds. Choppy cases with a 30-day rise gained 5.2 % over drift but with a day-clustered t of only 1.04 (74 cases, 32 days). Choppy cases with a 30-day fall gave a short gain of 5.3 % (t 1.94, 83 cases, 39 days). The top 30-day fifth gained 12.3 %, but with t 1.24.
- **F4:** The choppy fall-continuation is uneven across years. The short-side excess was -7.2 % in 2018 (t -3.18, 16 cases) and -13.6 % in 2021 (t -5.94, 25 cases). It was near zero in 2019 (-1.1 %, t -0.32) and 2020 (+1.5 %, t 0.38). These t-values are not clustered by day.
- **F5:** The book is a pure short book and does not earn what the idea measures.
- **F6:** Trade results do not grade with the entry forecast. The mean net result by quartile of entry forecast was -2.46 % at the deepest forecast (mean -15.2), +0.09 %, -3.74 %, and -2.41 % at the shallowest (-3.9). The book's linear sizing spreads its exposure over the many moderate falls, where F1 shows no follow-through, rather than the extreme ones.
- **F7:** Other angles did not stand out once the number of angles looked at is considered. These were:

## Ideas
- `067-01.b1.g1.b1.g1_deep-month-slide-accelerates` (from F1, F2, F5, F6): In a choppy market, a coin's fall over the past 30 days is followed by a further fall over the next 10 days. The follow-through grows more than in proportion to the depth of the fall, so that the deepest monthly slides carry almost all of the continuation and shallow slides little of it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
