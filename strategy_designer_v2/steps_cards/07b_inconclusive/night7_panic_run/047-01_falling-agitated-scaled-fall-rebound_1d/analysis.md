---
line: 7.b inconclusive
backtest: 047-01_falling-agitated-scaled-fall-rebound_1d
idea tested: 047-01_falling-agitated-scaled-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2201 USD
---
## Findings
- **F1:** In folds B and C, the in-profile down-day cases point the way the idea predicts but are too few to separate from 0. There are 209 cases on 90 days, with a mean unusual 3-day move of +0.85 % (t 0.64). This matches the full-test verdict, which is on the predicted side but short of the bar: +0.71 %, t 0.95, 223 case-days. The size is +0.86 % per case with t 1.70, 4.4 times the 0.19 % cost of a trade.
- **F2:** The grading the idea claims is present. In folds B and C, the slope of the unusual 3-day move on the scaled fall is +0.024 per unit (t 2.25, 209 cases). The two largest fall quartiles average +3.97 % (q3) and +1.33 % (q4) over 3 days against −0.15 % for q2, but each quartile has only 19 to 31 days, so no quartile alone is sure.
- **F3:** The effect is mixed across coins and years, which is why the t stays low. Over 3 days, ETH is +2.05 % (t 1.11) and XMR +2.21 % (t 0.99), while BTC is −0.31 % (t −0.21). The year 2020 (window w16) is +6.45 % (t 1.85), against 2019 at −1.86 % (t −1.26) and 2021 at −2.61 % (t −0.79). A few stressed windows carry most of the mean.
- **F4:** The rebound shows most clearly on the first day rather than over the plan's 3 days. After an in-profile down day, the next day's unusual move is +1.22 % (t 1.57), and it is +2.6 % for the two largest fall quartiles (t 1.62 and 1.51). The mean fades to +0.31 % at 5 days (t 0.21) and −0.22 % at 10 days.
- **F5:** The mirror side the brief names reverses on the next day and is graded. In-profile up days are followed by −1.48 % the next day (t −2.39, 209 cases, 95 days). The largest-rise quartile is followed by −2.95 % (t −2.16) and the third quartile by −2.22 % (t −2.49), against −0.43 % for the smallest-rise quartile.
- **F6:** The same down days outside the profile show no rebound, so the effect is specific to the falling, agitated profile as the brief claims. Outside it, the 3-day unusual move is −0.19 % (t −0.36, 1,096 cases on 328 days), and the largest-fall quartile is +0.83 % (t 0.77).
- **F7:** The test already used every fold available for its six coins. More data exists only as other coins: 13 more coins have daily bars, mostly in folds A and D (ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ in A and D, partly in B and C; NEAR, SUI, TAO, ONDO in D). The falling, agitated profile is rare (about 11 % of days), so these coins would add cases where too few is the problem.

## Ideas
- `047-01.b1_scaled-fall-rebound-more-coins` (from F1, F2, F3, F6, F7): In a falling, agitated market, a down day is followed by a rise over the next 3 days, and the larger the day's fall in units of its 30-day daily-return swing, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
