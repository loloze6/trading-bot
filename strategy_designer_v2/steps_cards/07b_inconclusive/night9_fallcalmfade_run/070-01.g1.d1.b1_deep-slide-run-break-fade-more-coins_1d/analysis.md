---
line: 7.b inconclusive
backtest: 070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins_1d
idea tested: 070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3468 USD
---
## Findings
- **F1:** Step 5's main measure is on the predicted side but short of the bar: +0.50 % unusual next-day move per short case, t 1.60, over 405 cases on 218 days. In folds B and C alone, the same next-day move is +1.32 % with t 2.45 (162 cases, 94 days). Working back from these, the 243 cases in folds A and D average about −0.05 %, so the effect sits in part of the data and is flat in the rest.
- **F2:** Inside folds B and C the effect varies by period: 2018 gives +2.37 % (t 2.52, 71 cases), 2019 gives +0.63 % (t 0.73), and 2021 gives +0.21 % (t 0.32, only 37.5 % of cases positive). Windows w12, w13 and w18 are near 0 (+0.30 %, +0.14 %, −0.02 %), while w7 gives +3.43 % (t 3.06).
- **F3:** The idea's grading by 20-day depth is not in the data. By 20-day return quartile, the deepest slide earns +0.96 % (t 0.78), less than the third quartile's +2.13 % (t 2.97). By forecast-size quartile the pattern is not monotonic (+2.56 %, +0.34 %, +1.73 %, +0.64 %).
- **F4:** The grading by run length does show. Up days ending runs of 2 or 3 down days earn +0.98 % (t 1.33, 83 cases) and +0.58 % (t 0.65, 44 cases). Runs of 4 earn +2.45 % (t 1.87, 14 cases), and runs of 5 or more earn +3.49 % (t 3.16, 21 cases on 20 days).
- **F5:** The fade keeps building past the plan's one-day horizon. In folds B and C the unusual move in the short direction is +1.32 % over 1 day (t 2.45), +2.17 % over 2 days (t 2.81) and +2.62 % over 3 days (t 3.00, 158 cases, 91 days, 67.7 % positive). Over 5 days it is +2.87 % (t 2.25).
- **F6:** Over 3 days the run-length grading holds at the extremes. Runs of 5 or more give +5.00 % (t 2.71, 20 cases), against +2.92 % for runs of 2 (t 2.24) and +1.13 % for runs of 3 (t 0.85).
- **F7:** Cost is not the obstacle. The full-data total move of +0.37 % per case is 1.6 times the 0.23 % cost of a trade. The book's Sharpe is 0.52, but its Calmar is only 0.35 and it is in a position on only 3 % of coin-days.

## Ideas
- `070-01.g1.d1.b1.b1_run-break-fade-three-days` (from F1, F4, F5, F6): In a falling, calm market, an up day that ends a run of down days is followed by a fall over the next three days, only while the coin's 20-day return is deeply negative. The fall is larger the more down days the run held beyond the first.
- `070-01.g1.d1.b1.b2_long-run-break-fade` (from F1, F3, F4): In a falling, calm market, an up day that ends a run of down days is followed by a fall over the next day, only while the coin's 20-day return is deeply negative. The fall is larger the more down days the run held beyond the first.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
