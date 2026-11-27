---
line: 7.g patterns
backtest: 086-02.c2_deep-down-day-continues_1d
idea tested: 086-02.c2_deep-down-day-continues
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3934 USD
---
## Findings
- **F1:** In the rising agitated profile, sampled every 5 days on its own grid, the days with the lowest closes within their range (bottom quartile of close location, 32 cases) were followed by a short-side excess move of +4.98 % over 5 days (t 2.98); the other three quartiles were near zero (-2.17 %, -0.48 %, -0.71 %, all |t| < 0.6). Low closes inside agitated uptrends kept falling. The held agitated long books (039-02, 045-01) buy these same days as rebounds, so this is the opposite side.
- **F2:** In the same profile, at a 5-day horizon, the 5-day short excess falls steadily across quartiles of the day's return scaled by its 30-day swing: +4.29 % (t 2.14), +2.27 %, -1.00 %, -4.95 % (25 cases each, Spearman -0.157, p 0.12). Deeper down days were followed by larger falls over the next 5 days. Over 10 days this grading disappeared (Spearman -0.19, p 0.17; step 5's deeper-minus-shallower was -1.13 %).
- **F3:** The tested 10-day short had no edge. Its unusual move was -0.16 % per case (t -0.10, 218 days). The total move was -1.32 %, against a cost of 0.37 % a trade. The book's Sharpe was -0.08.
- **F4:** The brief's own situation, a first down day after an up run of at least 2 days, had no edge in the profile at any horizon: short excess -0.32 % at 3 days, +1.34 % at 5 days and +0.31 % at 10 days (n 54, 50, 38; all |t| < 0.6). The run's size (Spearman with the run's swing-scaled return between -0.06 and +0.07) did not grade it either. Outside the profile the same days rose afterwards: -1.35 % at 3 days, t -2.05, n 179.
- **F5:** Several other angles in the profile showed nothing that stood apart from chance after about 40 comparisons:

## Ideas
- `086-02.c2.g2_deep-down-day-five-days` (from F2, F3, F4): In a rising, agitated market, the deeper a coin's down day, measured in units of its daily swing over the last 30 days, the more the coin falls over the next 5 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `086-02.c2.g1_rising-agitated-low-close-continues` (from F1, F3): In a rising, agitated market, the closer a coin's day closes to its low within the day's range, the more the coin falls over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
