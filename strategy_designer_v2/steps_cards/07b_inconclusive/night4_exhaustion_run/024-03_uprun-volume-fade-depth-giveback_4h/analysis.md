---
line: 7.b inconclusive
backtest: 024-03_uprun-volume-fade-depth-giveback_4h
idea tested: 024-03_uprun-volume-fade-depth-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3946 USD
---
## Findings
- **F1:** The tested short after up-runs sits on the predicted side but is too small to show: step 5 measured +0.13 % per case (t 1.15, 5709 cases, strength 0.014), below the 0.19 % cost of a trade, and my recomputation finds no horizon that does better (6 bars +0.01 % t 0.11, 12 bars +0.11 % t 1.20, 18 bars +0.14 % t 1.28, 36 bars +0.05 % t 0.29, about 5,600 to 5,800 cases each).
- **F2:** The gradient runs against the idea. The fall after up-runs comes from the small runs and turns into a rise after the large ones. By run_gain quintile the short-direction move is +0.28 %, +0.25 %, +0.77 % (t 3.22), −0.17 % and −0.41 % (t −1.48). By first-hit run size it is +0.80 % in the smallest quintile (t 3.46, 1054 cases) and −0.13 % in the largest. Streaks of 4 bars give −1.11 % and streaks of 6 or more give −1.96 %.
- **F3:** The up-side effect is mixed across periods and weak everywhere. By year it is +1.52 % in 2018 (t 3.83), +0.89 % in 2022 (t 3.02) and −0.82 % in 2020 (t −2.38), and it is near zero in 2023 to 2025. Every coin is positive, but no t exceeds 1.13 (LTC +0.30 %, BTC +0.04 %).
- **F4:** Volume fade adds little to the up side. Among the two largest run-size quintiles, the highest-fade tercile gives +0.56 % (t 1.56, 585 cases) against −0.15 % and −0.30 % for the other two. Cases in the top half of both run gain and fade give −0.46 % (t −1.31, 799 cases).
- **F5:** Falls behave the other way, as the brief says, and with a graded size. After an unbroken run of falling 4h bars, the 18-bar unusual move toward a rebound by loss-size quintile is −0.59 % (t −2.72), −0.31 %, −0.37 %, +0.01 % and +1.18 % (t 4.14, 1058 cases). The top quintile has a strength of 0.13 and a total move of +1.59 %, about 8 times the 0.19 % cost.
- **F6:** The rebound after large falls holds in most years and on every coin, but volume fade barely changes it.

## Ideas
- `024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins` (from F1, F3, F4): After an unbroken streak of rising four-hour periods whose gain is large relative to the coin's typical four-hour move over the past 30 days, the coin falls over the next three days. The more the volume declined from the start of the streak to its end, the larger the fall.
- `024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound` (from F5, F6): After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin rises over the next three days. The larger the streak's loss in typical four-hour moves, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
