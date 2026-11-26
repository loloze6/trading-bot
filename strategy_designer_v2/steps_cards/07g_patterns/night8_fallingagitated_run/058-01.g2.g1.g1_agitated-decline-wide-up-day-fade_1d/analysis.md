---
line: 7.g patterns
backtest: 058-01.g2.g1.g1_agitated-decline-wide-up-day-fade_1d
idea tested: 058-01.g2.g1.g1_agitated-decline-wide-up-day-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5762 USD
---
## Findings
- **F1:** The book's gain on up days sits almost entirely in the widest upper wicks. On in-profile up days, the position's summed one-day gain is 1.107 in the top quartile of the upper wick (high minus close, over the 30-day return standard deviation), out of 1.408 over all four quartiles (79 %). Its mean is +0.81 % a case there, against +0.04 %, +0.06 % and +0.12 % in the three lower quartiles.
- **F2:** In the falling agitated profile, an up day's next-day unusual move grows more negative with its upper wick: by quartile -0.47 %, -0.55 %, -0.73 % and -1.67 % (top quartile t -1.80, 136 cases, 72 days). Outside the profile the same quartiles give -0.16 %, -0.13 %, -0.22 % and -0.13 %, all |t| < 1.1 on 746 or 747 cases each.
- **F3:** Inside the profile, the size of the up day's close-to-close rise does not grade the next-day fall, while the day's range does. By the rise against the 30-day standard deviation, the quartiles give -1.25 %, -0.40 %, -1.62 % and -0.16 % (top quartile t -0.19). By the range, they give -0.24 %, -0.61 %, -1.03 % and -1.55 % (top quartile t -1.68), and the book's summed gain by range quartile rises from -0.017 to 1.010.
- **F4:** The fade lives in the profile. Up days inside the falling agitated profile are followed by a next-day unusual move of -0.98 % (t -2.54, 613 cases, 258 days); outside it, -0.14 % (t -0.89, 3,572 cases).
- **F5:** Down days in the profile rebound the next day by +1.28 % (t 3.25, 685 cases), graded by the size of the fall: by quartile from the largest fall, +2.54 % (t 2.31), +1.35 %, +1.55 % and +0.05 %. This is the falling agitated long rebound the profile map already holds 12 times, so it is not a discovery.
- **F6:** The brief's multi-day rise is not shown in these folds. The top quintile of the 3-day rise against the usual swing is followed by -2.21 % over 3 days (t -1.35, 73 cases on the 3-day grid). The top quartile of the 2-day rise is followed by +0.15 % over 2 days (t 0.14).
- **F7:** The one-day fade of the day's sign in the profile holds on every coin and every year. It is +1.12 % overall (t 3.90, 1,102 cases, 393 days). Five of six coins have t > 2 (LTC +1.75 % t 3.69; XRP +0.91 % t 1.31). Every year is positive, with 2018 at t 2.28 and 2020 at t 2.63.
- **F8:** No weekday pattern stands out: the next-day unusual move by weekday stays between -0.50 % and +0.41 %, all |t| < 1.6 on about 1,190 cases each.

## Ideas
- `058-01.g2.g1.g1.g1_agitated-decline-up-day-wick-fade` (from F1, F2, F3, F4, F7): In a falling, agitated market, an up day that closes well below its high, with its high-to-close distance measured against the standard deviation of its daily returns over the past 30 days, is followed by a fall over the next day; the longer that upper wick, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
