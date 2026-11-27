---
line: 7.g patterns
backtest: 070-01.b1.b1_calm-decline-depth-fade_1d
idea tested: 070-01.b1.b1_calm-decline-depth-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4306 USD
---
## Findings
- **F1:** In falling calm markets (bars in regime mean_reversion or unknown), up closes after at least two down closes are followed by a next-day move of −0.94 % beyond drift (t −2.46, 294 cases on 161 days). Outside the profile the same days fall −1.14 % (t −2.94, 889 cases on 359 days), so a break of a down run fades in every profile, not only in falling calm.
- **F2:** Inside the profile, the grading lives in the deepest runs. The deepest third of run losses is followed by −2.60 % (t −4.39, 57 days) and −2.69 % over 2 days (t −2.82). The middle third gives +0.41 % (t 0.87) and the shallowest third −0.63 % (t −1.09). The run's length in days grades nothing clean: 2 days −0.80 %, 3 days −0.33 %, 4 days −1.34 %, 5 or more −2.42 % (t −3.39, 33 days).
- **F3:** When the run's fall is scaled by the coin's 30-day swing (all breaks after at least one down close), the deepest quartile falls −1.06 % the next day (t −2.51, 192 days); the other quartiles give −0.52 %, +0.04 % and −0.37 %. Within that deepest quartile the fall lives in falling markets: proxy falling calm −1.72 % (t −2.53, 71 days), falling agitated −1.87 % (t −1.99, 60 days), rising calm −0.04 % and rising agitated −0.32 %. The full-sample correlation of scaled depth with the next-day move is −0.09 over 2,024 cases.
- **F4:** The effect leans heavily on one year. The deepest scaled quartile falls −3.67 % in 2018 (t −6.02, 52 days), −0.48 % in 2019, −1.25 % in 2020 and rises +0.68 % in 2021. The book's mean per position bar shows the same tilt: 1.40 % in 2018 against 0.23 to 0.30 % in 2019 to 2021.
- **F5:** Two other patterns did not stand out against the number of angles looked at. A down close after the strongest 3-day rise (top quintile of 3-day return over the 30-day swing) rose +0.94 % the next day (t 2.16, 169 days). Outside the profile, the largest one-day falls (lowest quintile of the day's return over the 20-day swing) rose +0.98 % (t 2.68, 366 days), but the map's agitated long cells already hold many fall-rebound books.
- **F6:** Weekday (largest |t| 1.78 in profile, Saturday), close position in the day's range (|t| at most 1.85) and relative volume (|t| at most 1.74) showed no next-day pattern that stands out.

## Ideas
- `070-01.b1.b1.g1_swing-scaled-calm-decline-fade` (from F2, F3, F1, F4): In a falling, calm market, a day that closes up after an unbroken run of down days is followed by a fall over the next day, and the larger that run's total fall measured against the coin's typical daily swing over the last 30 days, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
