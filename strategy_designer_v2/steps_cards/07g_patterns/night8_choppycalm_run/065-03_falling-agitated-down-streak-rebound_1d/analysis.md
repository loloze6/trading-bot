---
line: 7.g patterns
backtest: 065-03_falling-agitated-down-streak-rebound_1d
idea tested: 065-03_falling-agitated-down-streak-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4402 USD
---
## Findings
- **F1:** Inside the falling, agitated profile, the next-day excess return rises steadily with the raw count of consecutive lower closes: −0.91 % after a day that did not close down (t −4.3, 728 bars), then +0.74 % (t 2.7, 456), +1.20 % (t 3.7, 194), +1.99 % (t 2.0, 84) and +3.64 % (t 3.4, 48) for streaks of 1, 2, 3 and 4 or more days; the slope of next-day return on the raw streak is +1.07 % per day of streak (t 4.19, clustered over 499 days). Measured on all profile bars of folds B and C, this grading is the opposite of the verdict's slope on the standardised forecast (−0.0145 % per point, t −0.36).
- **F2:** After removing what the last day's scaled return predicts in the falling, agitated profile (its own slope is −1.16 % per usual swing, t −2.70, 410 days), streaks of 0 and 1 day still average −0.26 % and −0.25 %, while streaks of 2, 3 and 4 or more days average +0.22 %, +1.97 % and +2.34 % (167, 70 and 37 bars), so the length of the slide adds to the size of the last day.
- **F3:** The depth of the slide does not carry the effect the way its length does: in the falling, agitated profile the 5-day return scaled by the coin's swing has a next-day slope of −0.65 % (t −1.14, 232 days) and a 3-day slope of −0.50 % (t −0.33, 75 days), and its quintiles are not monotonic (+1.16 %, −0.21 %, −0.09 %, +0.84 %, −0.61 %).
- **F4:** Outside the profile the streak does not grade the next day (slope +0.087 % per day, t 0.85, 1404 days; streak 3 +1.21 % but streak 4 or more −0.51 %), so the counting effect lives in the falling, agitated market.
- **F5:** The book's gain is concentrated: window w16 sums +0.280 of the twelve windows' total daily return of about +0.62 (45 %), and next-day excess on held bars is +2.65 % in 2020 (t 5.9, 187 bars) against +0.32 % to +0.90 % in the other years. This concentration is consistent with the failed Calmar (0.63).

## Ideas
- `065-03.g1_down-close-count-rebound` (from F1, F2, F3, F4): In a falling, agitated market, the more of the last seven days a coin closed lower than the day before, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
