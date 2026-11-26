---
line: 7.g patterns
backtest: 031-02.b1.b1.b1.d1_small-body-wide-uprun-day_1d
idea tested: 031-02.b1.b1.b1.d1_small-body-wide-uprun-day
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4505 USD
---
## Findings
- **F1:** The idea's gain does not come from flat days. Among wide days (range at least 1.5 times the 20-day mean range) after a 5-day rise, days with a large body (flatness under 0.5) were followed by a 3-day unusual move of +2.11 % (t 2.28, 524 cases, 235 days), against +1.02 % (t 1.14, 329 cases, 169 days) for the flat days the idea selects.
- **F2:** Over a 20-day rise, the 3-day unusual move grows with the day's range against its 20-day mean range: -0.13 % at 1 or below (t -0.41, 2702 cases), +0.04 % from 1 to 1.5 (t 0.08, 1308 cases), +1.09 % from 1.5 to 2 (t 1.92, 541 cases), +1.99 % from 2 to 3 (t 2.07, 286 cases) and +5.78 % above 3 (t 1.80, 99 cases).
- **F3:** Over a 20-day fall or flat, the same wide days show nothing. The moves are -0.43 % (t -0.57), -0.75 % (t -0.45) and +3.56 % (t 1.20, only 65 cases on 21 days) for the widths from 1.5 to 2, from 2 to 3 and above 3.
- **F4:** Among all wide days (range at least 1.5 times the mean), the 3-day unusual move grows with the coin's 20-day return. By quintile from lowest to highest it is +0.85 % (t 0.56), -1.01 % (t -1.42), -0.02 % (t -0.03), +2.12 % (t 2.91, 174 days) and +3.70 % (t 2.59, 157 days), about 298 cases each.
- **F5:** On wide days, the sign of the 60-day return separates the outcomes in the same way: +2.54 % (t 2.76, 583 cases, 194 days) after a 60-day rise and -0.56 % (t -0.47, 351 cases) after a 60-day fall.
- **F6:** On wide days after a 5-day rise, a 20-day fall removes the effect: -0.68 % (t -0.53, 106 cases), against +2.02 % (t 2.78, 747 cases, 288 days) when the 20-day return is positive.
- **F7:** Wide days after a 20-day rise were positive in 6 of the 8 years. The two exceptions were 2018 (-2.86 %, 26 cases) and 2022 (-2.15 %, 72 cases), the two bear years, so the effect depends on the up-trend.
- **F8:** Narrow flat days do not mark the end of a run, which contradicts the brief's reversal reading. Days with a range under the 20-day mean and flatness of at least 0.5 were followed by -0.17 % after a 5-day rise (t -0.47, 1915 cases) and -0.17 % after a 5-day fall (t -0.44, 2078 cases).
- **F9:** The book's gain is concentrated in a few days. The best 5 % of its days add 218 % of its total gain and the worst 5 % take away 137 %, over 2898 days with a mean of +0.040 % a day.
- **F10:** On wide days, higher volume against the 20-day mean volume goes with larger moves, but no tercile is sure: +0.31 % (t 0.51), +1.15 % (t 1.79) and +1.92 % (t 1.58), about 497 cases each.

## Ideas
- `031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend` (from F1, F2, F3, F6, F7): In a coin whose 20-day return is positive, a day whose high-low range is wide compared with its average daily range over the past 20 days is followed by a further rise over the next 3 days, and the wider the range against that average, the larger the rise.
- `031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month` (from F4, F5, F6, F1): After a day whose high-low range is wide compared with its average daily range over the past 20 days, the coin rises over the next 3 days, and the larger its 20-day rise before that day, the larger the following rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
