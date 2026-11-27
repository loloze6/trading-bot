---
line: 7.b inconclusive
backtest: 036-02.g1_rising-agitated-scaled-rally-continuation_1d
idea tested: 036-02.g1_rising-agitated-scaled-rally-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3489 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar. Step 5 measured a mean unusual 3-day move of +1.67 % (t 1.62 over 193 case days, 240 cases, strength 0.176) with a positive slope (0.0016). In the explore half the 54 grid cases give +3.1 % at 3 days with t 1.43, and the result stays positive at every horizon from 2 to 7 days (+2.3 %, +3.1 %, +3.4 %, +2.2 %; t 1.44, 1.43, 1.19, 0.75).
- **F2:** The positive mean is carried by a few large moves, not by the typical case. At 3 days the median unusual move is -0.8 % and only 44 % of cases are positive. The standard deviation is 16.2 %, with the 10th to 90th percentile running from -14.4 % to +29.4 %. Without the 5 largest cases the mean is -0.5 %.
- **F3:** The effect is mixed across periods. Window w16 alone gives +11.4 % (t 2.37, 16 cases) and the year 2021 gives +6.5 % (t 1.86, 28 cases). Against that, w15 gives -6.9 % (t -1.98, 8 cases) and w7 (2018) gives -3.7 % (t -2.70, 5 cases). Too few windows hold cases for any one regime to be read as the effect's home.
- **F4:** The grading the idea claims does not show in the explore half. At 3 days the scaled-rise terciles give +0.1 % (low, 1.03 to 1.31 ranges), +6.2 % (mid) and -3.0 % (high, 2.0 to 5.2 ranges; t -1.06, 12 cases). The slope of the 3-day unusual move on the forecast is -0.0053 (t -0.93, 54 cases). Before the profile filter, the slope on the scaled rise is also flat (t from -0.85 to +1.19 across 1 to 7 days).
- **F5:** The test ran on far less data than the idea names and the data offers. The record holds BCH, DOGE and ZEC only in the explore half: 6, 2 and 12 windows, 2,436 bars. Only 117 bars of that half were in the trending regime inside the profile. The plan's six core coins have data in all four folds, and 13 more coins have data in folds A and D.
- **F6:** Size against cost is not the obstacle. The total move of +2.03 % per case is 5.5 times the 0.37 % trade cost, and the unusual move is 4.5 times it. The book's Sharpe of 0.60 failed on Calmar only (0.31), so a clear verdict on more data is what this idea needs.

## Ideas
- `036-02.g1.b1_scaled-rally-continuation-more-coins` (from F1, F2, F5, F6): In a rising, agitated market, a coin whose 3-day return is large against its 30-day mean daily high-to-low range keeps rising over the next 3 days, and the larger that range-scaled rise, the larger the further gain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
