---
line: 7.b inconclusive
backtest: 050-01_falling-calm-scaled-week-fall-continuation_1d
idea tested: 050-01_falling-calm-scaled-week-fall-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2807 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar: step 5's main measure is a +0.72 % short-direction excess over 3 days (t 1.59, 677 cases on 316 days), its size is +0.87 % with t 2.01 on 410 days (strength 0.099 of a usual 7.96 % move), and the slope on |forecast| is +0.00027 (t 0.66).
- **F2:** On folds B and C, 7-day falls in the falling calm profile are followed by a further fall at every horizon, but the independent evidence is thin: +0.49 % over 1 day (t 1.88, 379 days), +1.41 % over 3 days (t 1.91, 318 cases on only 131 days), +1.89 % over 5 days (t 1.65, 76 days) and +2.48 % over 7 days (t 1.09, 52 days).
- **F3:** The carry-on is graded in the predicted order but too noisy to separate. Over 3 days, the quartile with the largest scaled falls continues +2.39 % (t 1.27, 36 days) against +0.75 % for the smallest (t 0.81), all four quartiles are positive, and the slope is t 1.03 at 3 days and t 3.27 at 5 days.
- **F4:** The effect is not carried by one coin. Five of the six coins continue over 3 days: ETH +3.37 % (t 3.22, 53 days), ZEC +1.61 % (t 1.58), LTC +1.12 %, XMR +1.10 %, XRP +1.00 %; BTC alone is negative at -0.56 % (t -0.48, 31 days).
- **F5:** The falling calm profile is rare, which limits the evidence most. On folds B and C, 2018 gives 149 cases (+2.27 %, t 1.79) and 2019 gives 113 (+1.75 %, t 1.65), while 2020 and 2021 hold only 24 and 32 cases, both negative (-2.09 % and -1.15 %, |t| under 1.4). Most windows hold under 25 cases.
- **F6:** Per case, the total move of +0.48 % is 2.5 times the 0.19 % cost of a trade and the unusual move is 4.5 times it. The size is not what blocks the test; the number of independent days is, and the six coins already use all their folds. The other 13 coins with daily data in folds A to D add cases.

## Ideas
- `050-01.b1_calm-downtrend-fall-continuation-more-coins` (from F1, F2, F3, F4, F5, F6): In a falling, calm market, a coin that has fallen over the last 7 days keeps falling over the next 3 days, and falls further the larger its 7-day fall is in units of its 30-day daily-return swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
