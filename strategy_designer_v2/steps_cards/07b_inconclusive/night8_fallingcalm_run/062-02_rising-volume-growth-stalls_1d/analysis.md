---
line: 7.b inconclusive
backtest: 062-02_rising-volume-growth-stalls_1d
idea tested: 062-02_rising-volume-growth-stalls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3630 USD
---
## Findings
- **F1:** The test's measure is zero, not short of the bar. The slope of the 5-day unusual return on the forecast was +7.1e-05 with a day-clustered t of 0.18 over 1,345 cases on 409 days. The idea's size is +0.20 % per case (t 0.43, 646 days), a strength of 0.019, which is 1.0 times the 0.19 % cost of a trade.
- **F2:** In folds B and C the forecast's slope at 5 days reaches t 2.00, but only when cases are counted one by one (746 cases). Clustered by day, the raw volume-change slope in the rising profile falls to t −1.67 at 5 days (318 cases, 84 days) and t −1.40 at 10 days (158 cases, 42 days). With so few independent days the result cannot be told from noise.
- **F3:** The relation is not graded across volume change. At 5 days, the unusual move by quintile of the volume change, from most shrunk to most grown, is +4.8 % (t 2.17), −0.3 %, +0.8 %, +1.8 % and −1.1 %. Only the most-shrunk fifth stands out.
- **F4:** The one part that shows the effect rests on one window. Among rising-profile 5-day cases in the most-shrunk third, w11 holds 45 of 106 cases, with a mean unusual move of +7.3 %. The other 61 cases average about −0.3 %. w12, w14, w15 and w16 are negative (−1.5 %, −6.5 %, −4.9 % and −11.3 %).
- **F5:** The effect changes sign across periods and coins, so no regime or coin holds it.
- **F6:** Splitting by side does not settle it either. Shrink-only cases have a clustered t of +1.30 (149 cases, 61 days) and growth-only cases −1.48 (169 cases, 57 days). The long side's +1.75 % (t 2.36, 327 cases) comes from the same w11 cases as F4.
- **F7:** Outside the theme's profile, the falling profile gives the opposite sign. There, more volume growth is followed by a larger rise: t +2.55 at 5 days, +2.00 at 10 days and +2.94 at 20 days, counted one by one over 401, 193 and 99 cases. This is a different situation from the brief's and does not bear on it.

## Ideas
- No ideas: The theme's effect is not in the data. The tested measure is zero (t 0.18, F1), and no part of the rising market shows the shrinking-volume rise clearly. Its only strong cases sit in one window (F4), and its sign flips across windows, years and coins (F5, F6).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
