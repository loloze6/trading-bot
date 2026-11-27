---
line: 7.b inconclusive
backtest: 077-01.b1_choppy-agitated-width-graded-rebound_1d
idea tested: 077-01.b1_choppy-agitated-width-graded-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4071 USD
---
## Findings
- **F1:** On the predicted side but too weak overall: step 5 found +0.33 % mean excess next-day return (t 1.01, 409 cases, 280 days). In folds B and C the 66 cases average +2.05 % (t 2.27, 53 days), so the other folds dilute what shows here, and the test already used every fold and coin available on 1d.
- **F2:** The rise is carried by closes near the low: cases closing in the lowest quarter of the range average +3.54 % (t 2.92, 32 cases, 28 days), against +0.65 % (t 0.51, 34 cases) for closes from a quarter of the range to its middle.
- **F3:** The low-close rise holds every year seen: 2018 +4.76 % (3 cases), 2019 +3.44 % (t 2.33), 2020 +2.92 % (t 0.95), 2021 +3.95 % (t 2.23). The upper-low-half cases never pass +1.02 %.
- **F4:** The grading follows the close's distance from the middle (Spearman 0.24, p 0.049). Weighting by that distance raises the mean from +2.05 % to +2.70 %. By range bin, the 0.3 to 0.5 bin is flat (-0.15 %, t -0.16, 26 cases) while the three bins below 0.3 are +2.3 % to +5.1 %.
- **F5:** The test graded on the wrong width. The forecast's measure, the day's range over the 30-day return standard deviation, hardly predicts the rise (Spearman 0.12, p 0.43), and its quartiles do not rise in order (+0.19 %, +4.09 %, -0.78 %, +3.68 %). The day's range against its own 30-day mean range does predict it (Spearman 0.36, p 0.03).
- **F6:** The effect is spent within a day: the same cases average +2.05 % (t 2.27) over 1 day, -0.05 % (t -0.03) over 2 days and +0.66 % (t 0.59) over 3 days.
- **F7:** The same wide low closes in every profile rise less: +0.84 % (t 2.77, 1,259 cases), with no grading by close location (+0.89 %, +1.03 %, +0.68 % from the lowest bin up). The profile concentrates the effect fourfold, which is the brief's claim.

## Ideas
- `077-01.b1.b1_choppy-agitated-low-close-rebound` (from F1, F2, F3, F4, F6): In a choppy, agitated market, a wide day that closes in the lower part of its range is followed by a rise over the next day, larger the closer the close sits to the day's low.
- `077-01.b1.b2_width-vs-usual-range-rebound` (from F1, F5, F6): In a choppy, agitated market, a day that closes in the lower part of its range is followed by a rise over the next day, larger the wider the day's range against the coin's average daily range over the last 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
