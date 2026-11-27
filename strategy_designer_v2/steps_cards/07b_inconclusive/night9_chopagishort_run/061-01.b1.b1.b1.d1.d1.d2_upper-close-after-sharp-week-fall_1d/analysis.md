---
line: 7.b inconclusive
backtest: 061-01.b1.b1.b1.d1.d1.d2_upper-close-after-sharp-week-fall_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d2_upper-close-after-sharp-week-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3960 USD
---
## Findings
- **F1:** In folds B and C, how close the close sits to the day's high is what grades the fall. Cases closing in the top quarter of the range fall more than the drift over 3 days: +5.63 % (t 3.46, 87 cases on 46 days) for location 0.75 to 0.87, and +3.60 % (t 2.72, 62 cases on 39 days) for 0.87 to 1. Cases closing just above mid-range show nothing clear: +1.75 % (t 0.76) for 0.50 to 0.62 and +1.32 % (t 0.91) for 0.62 to 0.75. The rank correlation of location with the excess move is +0.094 over 338 cases.
- **F2:** The depth of the 5-day fall, which the test used to size its short, does not grade the move. The deepest quarter of falls gives the weakest result, +1.82 % (t 0.57, 85 cases), against +2.87 % (t 2.34) for the shallowest quarter. The rank correlations with the excess move have the wrong sign: +0.047 for the scaled 5-day return and −0.042 for |forecast|. This matches step 5's failed supporting check (above-median minus below-median |forecast|: −0.59 %).
- **F3:** Graded this way, the test's main measure drowns a real part of the effect. It is +0.44 % with t 0.78 over 1,255 cases on 423 days, and its strength is 0.061. In folds B and C the 3-bar grid cases average +2.76 % (t 2.31, 398 cases, 152 days), but only the upper-range half of them carries that number (F1).
- **F4:** The high-close cases are consistent from year to year. Cases with location at or above 0.75 fall more than the drift in every year: +4.9 % (2018, 47 cases), +2.2 % (2019, 26), +4.9 % (2020, 31) and +6.0 % (2021, 45). Cases below 0.75 turn negative in 2021 (−2.3 %, 62 cases).
- **F5:** Counted from each entry, the fall builds beyond the plan's 3 days. The excess short-side move is +2.94 % (t 2.56, 413 cases, 154 days) at 3 days and +3.59 % (t 3.15, 406 cases, 151 days) at 5 days, then stops growing at 10 days (+3.69 %, t 2.68).

## Ideas
- `061-01.b1.b1.b1.d1.d1.d2.b1_post-drop-high-close-graded-fade` (from F1, F2, F3, F4): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been a deep fall, its price falls over the next three days, and the nearer the close is to the day's high, the larger the fall.
- `061-01.b1.b1.b1.d1.d1.d2.b2_post-drop-high-close-five-day-fade` (from F1, F4, F5): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been a deep fall, its price falls over the next five days, and the nearer the close is to the day's high, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
