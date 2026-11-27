---
line: 7.g patterns
backtest: 067-02.b1.b1.b1.b1_agitated-chop-downside-more-coins_1d
idea tested: 067-02.b1.b1.b1.b1_agitated-chop-downside-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5825 USD
---
## Findings
- **F1:** The tested profile is too rare to judge: only 86 of 1,950 non-overlapping 5-day grid cells (4 %) were in the choppy-agitated profile. Inside it, both sides of the 20-day average fell over the next 5 days (above: −7.2 %, t −2.4, 8 cases on 7 days; below: −12.2 %, t −1.6, 18 cases on 11 days). So the profile's own fall, not the stretch, carried the short book's cases, and the book's 213 short trades lost 3.5 % on average before fees.
- **F2:** In choppy markets (60-day return between −10 % and +10 %, calm or agitated), the 5-day unusual move rises steadily across the quintiles of the stretch from the 20-day average in usual daily moves: −13.4 % (t −3.5, 19 cases), −4.0 % (t −2.7), −1.8 %, +1.9 %, then +6.5 % (t 2.0, 27 cases). The pattern is graded and runs on both sides, as the brief says.
- **F3:** Over 10 days the choppy-market grading is stronger. The slope of the unusual move on the stretch is +0.042 per usual move outside the agitated profile (t 4.65, 63 cases on 29 days, Spearman 0.47) and +0.037 inside it (t 3.1, 14 cases on 8 days).
- **F4:** The same 10-day slope is near 0 in falling markets (−0.001, t −0.05, 209 cases) and weaker in rising markets (+0.018, t 2.2, 188 cases). The carry belongs to the choppy trend, not to every market.
- **F5:** In choppy calm markets the grading comes mostly from closes above the 20-day average: 10-day slope +0.036 (t 3.4, 34 cases on 18 days), against +0.022 (t 0.7, 29 cases) below it. Over 5 days it is +0.025 (t 2.1) above against +0.006 (t 0.5) below.
- **F6:** The choppy-market carry is uneven across folds. The 10-day slope is +0.015 in fold B (t 0.8, 48 cases) and +0.057 in fold C (t 11.7, 29 cases on 12 days); the 5-day slope is +0.006 (t 0.8) in B and +0.038 (t 3.2) in C. Its sign is the same in both, but the strength rests mainly on one fold.
- **F7:** The moves at stake are far larger than a trade's cost. In choppy markets the outer stretch bins move −12.5 % (stretch below −2, 21 cases) and +6.5 % (above +2, 27 cases) over 5 days, against a cost of 0.23 % a trade. Size is not what failed this book; the side and the profile were.

## Ideas
- `067-02.b1.b1.b1.b1.g1_choppy-stretch-carries-ten-days` (from F2, F3, F4, F6, F7): In a choppy market, the further a coin's close stands from its 20-day average, counted in units of its 20-day standard deviation of daily returns, the further the coin keeps moving the same way over the next 10 days: up after closes above the average, down after closes below it.
- `067-02.b1.b1.b1.b1.g2_choppy-calm-upside-stretch-continuation` (from F5, F3, F6): In a choppy, calm market, the further a coin's close stands above its 20-day average, counted in units of its 20-day standard deviation of daily returns, the more the coin rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
