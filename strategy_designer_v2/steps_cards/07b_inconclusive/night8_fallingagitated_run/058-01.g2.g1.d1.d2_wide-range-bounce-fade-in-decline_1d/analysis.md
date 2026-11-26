---
line: 7.b inconclusive
backtest: 058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline_1d
idea tested: 058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 1
cost: 0.2172 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls just short of the bar: the mean unusual move per case in the short direction is +0.74 %, with a day-pooled t of 1.93 against a threshold of 2. The supporting check passes, at +1.36 % above the median against below it. The sample is 486 cases on 279 case-days, from only the six core coins, while 13 more coins have daily data in some or all folds.
- **F2:** The effect is graded as the idea says. It sits almost entirely in the strongest cases.
- **F3:** The effect is real but thinly spread, so this sample cannot show it clearly.
- **F4:** The plan measured the effect at the right horizon.
- **F5:** The effect is stronger when the 3-day fall is deeper.
- **F6:** Size is not the problem. The full-sample unusual move is +1.18 % per case (t 2.50, 207 days; 0.248 of the usual move), which is 6.1 times the 0.19 % cost of a trade. The book already passed step 6 with a Sharpe of 0.83. The test lacks cases, not size.

## Ideas
- `058-01.g2.g1.d1.d2.b1_wide-bounce-fade-all-coins` (from F1, F2, F3, F6): In a falling, agitated market, a coin's up day that comes while its 3-day return is still negative is followed by a fall over the next day, and the wider that day's high-to-low range against the standard deviation of its daily returns over the past 30 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
