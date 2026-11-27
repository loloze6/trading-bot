---
line: 7.b inconclusive
backtest: 067-01.b1.g1.b1.d1.d2_proportional-month-slide-continues_1d
idea tested: 067-01.b1.g1.b1.d1.d2_proportional-month-slide-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3805 USD
---
## Findings
- **F1:** The test's main measure is on the side the idea predicts but well short of the bar: mean +0.0121 with t 1.21 on 150 case-days. The tested run already used every fold (A to D) and all 19 coins, so no more data is available to add.
- **F2:** The proportional claim fails at the mild end. In folds B and C, the 10-day short gain over drift by depth quartile of the 30-day fall is +4.6 % in the deepest quartile (raw fall −61 %, t 0.33, 13 days), +12.2 % in q2 (−39 %, t 4.72, 19 days), +4.2 % in q3 (−19 %, t 1.11, 21 days) and −4.6 % in the mildest (−5 %, t −1.35, 20 days). This matches step 5's moderate half (−0.75 %) against its deep half (+2.33 %).
- **F3:** The effect grades more cleanly when the fall is measured against the coin's own daily swing over the same 30 days. By quartile of that scaled fall, the 10-day short gain over drift is +8.3 % (scaled fall −2.09, t 1.39), +5.9 % (−1.33, t 1.82), +4.9 % (−0.77, t 0.94) and −2.4 % (−0.28, t −0.77). The rank correlation is 0.27, against 0.26 for the raw fall.
- **F4:** The raw deepest falls are carried by few days. The deepest raw quartile gains +2.0 % at t 0.33 on 13 days, while large falls in a calm month gain +12.1 % (t 4.22, 14 cases, 9 days). Shallow falls stay near zero whether the month was calm (+0.3 %) or agitated (−1.9 %).
- **F5:** The effect is uneven over time but shows across the coins. By year, the 10-day short gain is +7.7 % (2018, t 2.80), +0.9 % (2019), −0.8 % (2020) and +5.6 % (2021). Over 5 days it is +4.0 % with t 1.75, against +3.4 % with t 1.28 over 10 days and +2.6 % with t 0.59 over 20 days, so the move shows mostly in the first days.

## Ideas
- `067-01.b1.g1.b1.d1.d2.b1_swing-scaled-month-slide-continues` (from F2, F3, F4): In a choppy market, the larger a coin's fall over the past 30 days measured against its own daily swing over those 30 days, the more it keeps falling over the next 10 days.
- `067-01.b1.g1.b1.d1.d2.b2_scaled-slide-five-day-continuation` (from F3, F5): In a choppy market, the larger a coin's fall over the past 30 days measured against its own daily swing over those 30 days, the more it keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
