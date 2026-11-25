---
line: 7.g patterns
backtest: 032-02_low-range-decline-continues-more_1d
idea tested: 032-02_low-range-decline-continues-more
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3574 USD
---
## Findings
- **F1:** Among coins whose 28-day return is at or above 0, the closer the close sits to its 28-day high, the larger the drift-adjusted 5-day return that follows (630 non-overlapping 5-day cases, OLS t 3.71, Spearman 0.145). The quintiles rise steadily from -2.63 % (t -2.22) for the furthest below the high to +4.06 % (t 2.97) for the nearest, against a trade cost of 0.19 %; these t's count cases on several coins the same day separately.
- **F2:** The F1 grading points the same way on all 6 coins (t 0.53 to 2.82) and in 2019, 2020 and 2021 (t 1.33, 3.18, 2.01). It reverses in 2018 (t -0.46, 49 cases) and in window w14 (t -2.78, 22 cases), and the 14-day version gives the same quintile ladder (-2.22 % to +4.39 %, top t 3.16).
- **F3:** Among coins with a 28-day return at or above 0, calmer 28-day high-low ranges against their 90-day norm are followed by larger 5-day rises (OLS t -3.25, 572 cases), with the calmest quintile at +4.04 % (t 2.86). With closeness to the 28-day high in the same regression, both hold: closeness t 3.08, calm ranges t -2.24. The sign reverses in w14 (t +2.28) and in 2018 (t +2.18).
- **F4:** The tested effect is absent inside declines: among coins down over 28 days, the calmness ratio does not grade the next 5-day return (component t -0.67, recomputed range ratio t 0.76, 501 to 579 cases), and step 5's slope t is -0.73 with an unusual move of +0.10 % (t 0.22).
- **F5:** Inside declines, distance from the 28-day high is not graded either: the quintiles run +0.88 %, -2.08 %, -2.60 %, -1.20 %, +1.28 %, a hump rather than a slope (116 cases each).
- **F6:** The short trades lose most at middling forecast sizes. The middle two quartiles of absolute entry forecast average -4.43 % and -4.40 % net per trade (176 and 170 trades), against -0.48 % for the smallest quartile and +0.18 % for the largest, so the book's loss does not shrink as the short grows.

## Ideas
- `032-02.g1_uptrend-near-high-continues` (from F1, F2, F4): Among coins that have risen over the past 28 days, the closer the day's close is to the highest close of those 28 days, the larger the further rise over the next 5 days.
- `032-02.g2_calm-uptrend-keeps-rising` (from F3, F4, F6): Among coins that have risen over the past 28 days, the smaller their daily high-low ranges over those 28 days compared with their own ranges over the past 90 days, the larger the further rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
