---
line: 7.g patterns
backtest: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound_4h
idea tested: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4050 USD
---
## Findings
- **F1:** The coin's past 3-day return, measured in its usual 3-day moves, grades the next 3 days. On the 18-bar grid the top quintile (mean +1.50 usual moves) is followed by an unusual move of +0.92 % (t 3.10, 1059 cases), against −0.60 % to −0.34 % in quintiles 2 to 4. The rank slope holds on all three grid offsets (t 3.90, 4.46, 5.66, about 5300 cases each). It survives averaging over coins at each date (+0.93 %, t 2.30, 482 dates), and is positive in 6 of 8 years (2020 t 3.02, 2023 t 2.72, 2024 t 2.86).
- **F2:** Volume rising behind the move adds to it. The top quintile of the ratio of the last bars' volume to the preceding volume is followed by +0.96 % (t 3.63, 1087 cases), against −0.69 % in the second quintile. The ratio keeps t 3.26 next to the past 3-day return in a joint regression. Its rank slope is weaker on the other grid offsets (t 2.17 and 2.08) and averaged by date (t 1.54).
- **F3:** The strongest cell combines the two: a past 3-day rise in the top quintile with volume in the top tercile is followed by +1.62 %. Among the deepest up-streaks, those with rising volume are followed by +1.09 % (406 cases) and those with fading volume by −0.45 % (256 cases). This is the opposite of the brief's fade-and-give-back.
- **F4:** The tested situation carries no graded rebound. Down-streak length shows no ordering: 1 bar −0.53 % (t −2.49), 2 bars +0.23 %, 3 bars −0.36 %, 4 bars +1.35 % (t 1.46, 127 cases). The tested idea's size is 0.007 of a usual move, with an unusual move of +0.05 % against a 0.19 % cost.
- **F5:** The book is mostly the coin's own drift. Its mean daily return per coin is close to holding: BTC 0.175 % vs 0.118 %, ZEC 0.143 % vs 0.155 %. Its worst 1 % of days are −17.1 % while the coin falls −15.2 %, and its yearly means follow the coin's (2018 −0.32 % vs −0.33 %, 2022 −0.15 % vs −0.17 %), which is why its Calmar is 0.35.
- **F6:** Recent volatility above its 30-day level grades the next 3 days weakly. The top quintile of 5-day volatility over 30-day volatility is followed by +0.76 % (t 2.44), but the quintiles are not ordered (−0.45 %, −0.43 %, +0.11 %, −0.28 %). The rank slope weakens on the other grid offsets (t 3.11, 2.12, 2.00).
- **F7:** Weekday patterns appear but do not hold up under the number of cuts made (7 weekdays × several measures). Grid cases starting Sunday are followed by −1.23 % (t −3.92), and next-day moves after a Friday close by +0.31 % (t 3.76). Next-day moves alternate in sign across the week with no mechanism, so I do not treat them as findings to build on.

## Ideas
- `024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound.g1_volume-backed-rise-keeps-rising` (from F1, F2, F3): The larger a coin's 3-day rise in units of its usual 3-day move, the more it keeps rising over the next three days, and the more so the higher its last day's volume stands against its volume over the preceding six days.
- `024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound.g2_three-day-rise-momentum` (from F1, F4): The larger a coin's 3-day rise in units of its usual 3-day move, the larger its rise over the next three days.
- `024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound.g3_rising-volatility-precedes-gains` (from F6): The higher a coin's 5-day volatility stands against its 30-day volatility, the more the coin rises over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
