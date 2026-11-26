---
line: 7.g patterns
backtest: 058-01.b1_calm-downtrend-all-coins_1d
idea tested: 058-01.b1_calm-downtrend-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4084 USD
---
## Findings
- **F1:** Inside the falling-calm profile, the coin's last 10-day return predicts its 5-day excess return on the non-overlapping 5-day grid with a positive slope of 0.126 (day-clustered t 2.13, 390 cases on 127 days), and the 3-day return does the same (slope 0.222, t 1.99, 407 cases on 132 days). The deeper the recent fall, the lower the next 5 days. The same slopes outside the profile are flat: r10p 0.014 (t 0.42) and r3p −0.012 (t −0.23), over 1,396 to 1,461 cases.
- **F2:** The tested 30-day depth carries almost none of this. Its slope inside falling calm is 0.035 (t 0.73, 344 cases on 111 days), in line with step 5's slope t of −0.61. Its 30-day quintiles are not ordered: −0.2 %, −1.6 %, −3.9 %, +1.1 % and +1.1 % from the deepest fall to the shallowest.
- **F3:** The recent-move effect is graded on its falling side. On the 5-day move scaled by the coin's 20-day swing, the two most-fallen fifths end −2.8 % (t −1.32, 33 days) and −3.0 % (t −1.84, 46 days) against drift over 5 days, while the top fifth ends +1.2 % (t 0.60). Leaving any one coin out keeps the slope between 0.0156 and 0.0192 (t 1.60 to 1.99).
- **F4:** The pattern is not steady by year, so it is weak evidence. The scaled 5-day slope in falling calm is +0.022 (t 1.63) in 2018, −0.003 in 2019, −0.011 in 2020 (9 days only) and +0.017 (t 0.91) in 2021.
- **F5:** The brief's volume split is contradicted. Among deeper-than-median 30-day falls in falling calm, those on the heaviest third of 10-day volume against 60-day volume end −2.5 % (t −2.01, 63 cases). That matches or exceeds those on the lightest third, which end −2.2 % (t −1.80, 57 cases).
- **F6:** The falling-calm excess return flips sign by year: −1.2 % in 2018, −2.2 % (t −3.42) in 2019, +4.0 % (t 3.21) in 2020 and +2.2 % (t 2.05) in 2021. This is why the 30-day short book earned only +1.8 % a year with a Calmar of 0.09.
- **F7:** The other patterns seen do not stand out against the many angles looked at, or are already held:

## Ideas
- `058-01.b1.g1_calm-downtrend-recent-fall-continues` (from F1, F2, F3, F4): In a falling, calm market, the more a coin has fallen over its last 10 days, the more it keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
