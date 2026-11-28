---
line: 7.g patterns
backtest: 032-01.b1_calm-fall-continuation-all-coins_1d
idea tested: 032-01.b1_calm-fall-continuation-all-coins
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3964 USD
---
## Findings
- **F1:** In falling calm markets, a coin's 3-day return grades its next 3 days: on the non-overlapping 3-day grid, the fallen third (3-day return about -4.6 % or worse) is followed by -1.46 % against drift (t -1.90, 61 cases) and the risen third by +1.84 % (t 2.15, 61 cases). The Spearman rho is 0.167 (p 0.024, 182 cases on 126 days). The pooled slope is 0.19, with an OLS t of 2.22 but only 1.66 when cases are clustered by day.
- **F2:** The grading holds across neighbouring choices but is weak on its own:
- **F3:** The short side alone, shorting the fallen third, earns +1.46 % per case over 3 days, about 5 times the 0.29 % cost of a trade, but its t with each day's cases taken together is only 1.57 over 48 days.
- **F4:** Outside falling calm markets the same 3-day grading is much weaker: rho 0.034 (p 0.26, 1,099 cases), with thirds at -0.53 % and +0.78 %. The short-horizon continuation is specific to the falling calm profile.
- **F5:** The tested 30-day fall does not grade the next day in falling calm markets:
- **F6:** Other angles showed nothing that stands out after this many looks:

## Ideas
- `032-01.b1.g1_calm-decline-recent-fall-continuation` (from F1, F2, F3, F4, F5): In a falling, calm market, the more a coin has fallen over its last 3 days, the more it keeps falling over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
