---
line: 7.b inconclusive
backtest: 058-01.g2_agitated-decline-one-day-rise-fades_1d
idea tested: 058-01.g2_agitated-decline-one-day-rise-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3469 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar: on all four folds the 694 short cases (379 days) gave back +0.33 % of unusual move over 3 days (strength 0.039 of a usual 7.96 % move, t 0.73). In folds B and C alone, the plan's own cases rebuilt from the forecast give +1.19 % (strength 0.13, t 1.18, 237 cases on 103 days), so the sign is the same on the folds shown.
- **F2:** The effect is spread thinly rather than sitting in one part of the data. In folds B and C, 5 of the 6 coins have a positive 3-day unusual move after the plan's cases, from +0.93 % (BTC) to +2.29 % (XMR) and +2.11 % (ZEC), with every coin's t under 1.5. ETH is the exception at -0.40 % (t -0.31). On the 3-day grid of up days in the profile, every year from 2018 to 2021 is positive (+2.67 %, +0.90 %, +0.80 %, +0.20 %), with each t under 1.1.
- **F3:** The grading is mixed, so the supporting check failed. On all folds the larger half of |forecast| minus the smaller half is -0.19 %. On the plan's cases in folds B and C it is -0.57 %, with the top quartile of the rise weakest (+0.28 %, t 0.18 vs +1.30 % to +1.64 % in the others). Yet on the 3-day grid of all up days in the profile, the quartiles of the rise in 30-day standard deviations rise in order: -2.60 %, +0.69 %, +2.39 %, +4.06 % (t -1.61, 0.48, 1.78, 1.97; about 44 cases each). The grading the idea claims is in the data in one sample and not in the other, and both samples are small.
- **F4:** The give-back shows most clearly over the next day, but without grading. On the 1-day grid, up days in the profile are followed by +0.99 % unusual fall (strength 0.19, t 2.26, 500 cases on 195 days). By quartile of the rise this is +1.02 %, +0.64 %, +1.66 %, +0.65 %, so it does not grow with the rise.
- **F5:** The market's own fall drowns the edge for the book. The normal drift in the short's direction is -0.39 % per 3 days, so the total move is -0.06 % per case, -0.3 times the 0.19 % cost of a trade. The unusual move alone is 1.7 times that cost, and the book's Sharpe is -0.16. More cases are what can tell the +0.33 % from zero; this test used only the six default coins on daily bars, while 13 more coins have daily data in folds A and D (and some in B and C).

## Ideas
- `058-01.g2.b1_one-day-rise-fades-wider` (from F1, F2, F3, F5): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall in its price over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
