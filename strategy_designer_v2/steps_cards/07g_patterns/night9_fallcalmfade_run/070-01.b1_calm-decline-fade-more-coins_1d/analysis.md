---
line: 7.g patterns
backtest: 070-01.b1_calm-decline-fade-more-coins_1d
idea tested: 070-01.b1_calm-decline-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4481 USD
---
## Findings
- **F1:** Among the run-break days in the falling-calm profile, the next-day move beyond the drift is graded by how deep the down run was, measured as its cumulative log fall over the coin's 20-day daily swing. The slope is -0.56 % per swing unit (t -4.35, 525 cases). This is stronger than the slope on run length in days, -0.38 % per day (t -2.73).
- **F2:** By quartile of that depth, the in-profile next-day excess return falls steadily: +0.33 % (t 0.59, 73 days), +0.04 % (t 0.08), -0.88 % (t -1.91, 89 days) and -1.20 % (t -2.41, 94 days). The deepest quartile's move is about 5 times the 0.22 % cost of a trade, while the tested idea's average case moves only +0.04 % (t 0.24).
- **F3:** By run length in the profile, 1-day runs (259 cases) are followed by -0.04 % (t -0.09) and runs of 5 or more days by -2.42 % (t -3.24, 33 days). Over 2 days the 5+ runs give -3.52 % (t -3.43). The flat average of the tested book comes from short runs, which make up most of its cases.
- **F4:** The same depth grading holds outside the profile (slope -0.37 %, t -3.17, 1968 cases) and over all profiles (slope -0.42 %, t -4.67, 2493 cases). So it is not specific to calm markets.
- **F5:** Outside the falling-calm profile, run-break days in a falling 60-day trend, which there means falling agitated, are followed by -1.83 % the next day (t -2.94, 244 cases on 81 days). In a rising trend they are followed by +0.23 % (t 0.59). The fade lives where the coin has been falling, not where it has been rising.
- **F6:** The effect is uneven across years. In-profile breaks give -1.40 % (t -2.42) in 2018, -0.31 % in 2019, +0.87 % in 2020 and +0.26 % in 2021. Runs of 4 or more days are negative in every year: -2.80 %, -1.28 %, -0.09 % and -1.93 %.
- **F7:** Other angles showed nothing that clearly stands out from chance, given how many were looked at. These were weekday in the profile (largest t +1.78), close position in the day's range in the profile (|t| at most 1.76), and ongoing down-run days in the profile (|t| at most 0.93). The out-of-profile rebound after the largest falls (lowest quintile +1.09 %, t 2.91) repeats the falling-agitated long rebounds the map already holds.

## Ideas
- `070-01.b1.g1_calm-decline-depth-fade` (from F1, F2, F3, F6): In a falling, calm market, a day that closes up after a run of down days is followed by a fall over the next day, and the deeper that run's total fall measured against the coin's usual daily swing over the past 20 days, the larger the next day's fall.
- `070-01.b1.g2_falling-market-depth-fade` (from F4, F5, F1): In a falling market, a day that closes up after a run of down days is followed by a fall over the next day, and the deeper that run's total fall measured against the coin's usual daily swing over the past 20 days, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
