---
line: 7.b inconclusive
backtest: 067-02.b1.b1.d1.g1_choppy-agitated-month-falls-continue_1d
idea tested: 067-02.b1.b1.d1.g1_choppy-agitated-month-falls-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2255 USD
---
## Findings
- **F1:** Step 5's main measure is on the predicted side but cannot be told from zero: the mean unusual move in the short direction is +0.54 % per case over 7 days, with t 0.43 over 215 cases on 108 days. The test already used every fold and every coin, so no more data is available to sharpen it.
- **F2:** The graded part of the idea is not in the data. Inside choppy agitated bars in folds B and C, the 30-day return and the next 7-day return have a correlation of 0.013 (36 grid cases). Across the depth quartiles of the falls, the shallowest quartile's unusual move (+8.2 %, t 2.10, 8 cases) matches q3 (+8.2 %) and exceeds q2 (+5.3 %). Only the deepest quartile is larger (+15.2 %, t 1.26, 8 cases on 5 days).
- **F3:** The fall that follows looks like the profile's own decline rather than a continuation of the month's fall. In the same profile, coins that had risen over the month also fell over the next 7 days: +5.3 % in the short direction, 6 cases, against +9.4 % after falls, 30 cases on 16 days, t 1.74. Over 14 days the deeper and shallower halves of the falls give almost the same move (+13.8 % and +13.4 %).
- **F4:** The visible gain rests on a few days and one episode. In w16 a single day carries 5 of the 30 cases at +32.9 % each, about 59 % of the summed move. Without it the remaining 25 cases average about +4.7 %. 2019 gives +1.7 % (t 1.19, 11 cases), and w15 gives +0.4 % (t 0.43, 8 cases).
- **F5:** Outside the choppy agitated profile, falls of the same depth show no ordered continuation over 7 days. The deepest quartile gives −0.9 % in the short direction (t −0.32, 111 cases). The middle quartiles give +3.4 % and +2.6 %, and the shallowest gives +0.5 % (t 0.32). So no other profile holds the graded effect either.

## Ideas
- No ideas: The tested result is on the idea's side but near zero (t 0.43) on all the data available, and nowhere in the data do deeper monthly falls lead to larger falls over the next week (correlation 0.013, F2, F5); the only fall seen follows the choppy agitated profile whatever the month's sign (F3) and rests on one episode (F4), so the theme's graded effect is not in the data.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
