---
line: 7.b inconclusive
backtest: 031-03.g1.b1.d2.e1_rally-on-fading-volume-fails_1d
idea tested: 031-03.g1.b1.d2.e1_rally-on-fading-volume-fails
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4273 USD
---
## Findings
- **F1:** Step 5's result is on the predicted side but indistinguishable from zero: the unusual move is +0.10 % per case over 14 days (t 0.09, 1225 cases on 645 days, strength 0.018). My rebuild of its cases gives the same, +0.005 % (t 0.004, 1177 cases on 614 days).
- **F2:** The one clear-looking reading does not hold up. In the situation (14-day return up, 14/30 volume ratio below 0), the short-side move on the grid starting at each window's first bar is +3.9 % over 14 days (t 2.19, 331 cases, 79 days). Averaged over all 14 grid offsets it is −0.28 % (mean t −0.04, about 238 cases per offset), so that grid's t is luck of the grid's placement.
- **F3:** The effect does not grow with the drying. Among the step-5 cases, by volume-ratio quartile from driest to mildest, the short-side move is +3.9 % (t 2.01), −1.4 % (t −0.72), +0.8 % (t 0.54) and +2.2 % (t 1.48). By forecast quartile from deepest to shallowest it is +2.8 % (t 2.17), −3.9 % (t −1.34), +0.5 % and +0.6 %. The volume ratio correlates with the short-side move at only −0.08 and −0.03 in the two 60-day regimes.
- **F4:** No regime holds the effect steadily. Among step-5 cases with the 60-day return down, the short-side move is +1.6 % (t 0.84, 267 cases); with it up, −0.4 % (t −0.18). Within the 60-day-down cases the yearly reading swings from −13.6 % (t −3.18) in 2020 to +11.2 % (t 3.58) in 2025. Over all 14 grid offsets the 60-day-down situation averages t 0.19, and its drier half averages t 0.31.
- **F5:** The brief's own reversal shows no clean lean against the 60-day move. Over 14 days, every quintile of the per-coin standardised 60-day return has a long-direction excess move within ±2.1 % with |t| ≤ 0.51 (about 184 cases each). Over 28 days the two extreme quintiles both rise: the biggest falls by +4.0 % (t 0.52) and the biggest rises by +16.1 % (t 1.36). That is the same sign at both extremes, not a reversal.
- **F6:** Even if the effect were real, it is too small to pay. The unusual move is 0.4 times the 0.22 % cost of a trade. The coin's normal drift against the short is −2.47 % per 14 days, which makes the total move −2.38 %, so the book lost money: Sharpe −0.42 and −11.5 % a year.

## Ideas
- No ideas: The test already used every coin, fold and the daily bars available. Its result is essentially zero, and no coin, year, regime, horizon or drying depth shows the effect steadily once grid placement is varied (F2–F4), so there is no part of the data to narrow the idea to and no more data to rerun it on.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
