---
line: 7.b inconclusive
backtest: 077-01.b1_swing-rise-carry-more-coins_1d
idea tested: 077-01.b1_swing-rise-carry-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3699 USD
---
## Findings
- **F1:** Inside the choppy calm profile, the 14-day return over the 30-day swing (scaled by sqrt 14) predicts the unusual 7-day move across its whole range: slope 0.050 per swing unit, t 3.48 (143 non-overlapping cases on 61 days, Spearman 0.30). The tested idea's threshold of at least 2 kept almost none of these cases: in folds B and C only 6 grid cases fall at 2 or above, all on 2 days of 2021. The plan's 76 cases on 64 days over all four folds give the step-5 t of 0.83.
- **F2:** The carry belongs to the profile. Outside choppy calm, the same slope at 7 days is 0.013 with t 1.31 (838 cases, 154 days), against 0.050 with t 3.48 inside it. At 5 and 10 days the inside slope is also stronger: 0.036 (t 2.24) and 0.055 (t 2.26), against 0.010 and 0.017 outside.
- **F3:** On the rising side, the effect shows below the tested threshold and is graded from small rises up. Inside the profile, at 7 days, the unusual move is +0.6 % for a scaled rise of 0 to 1 (t 0.35, 55 cases), +5.3 % for 1 to 2 (t 1.46, 18 cases) and +19.4 % for 2 to 3 (6 cases). The slope on positive values alone is 0.064 with t 2.96 (79 cases, 37 days). Cases above 1 move +8.8 % (t 1.93, 24 cases, 12 days).
- **F4:** The falling side points the same way but more weakly. Inside the profile, scaled moves below -0.5 are followed by an unusual 7-day move of -3.1 % (t -1.87, 30 cases, 22 days) and -6.2 % at 10 days (t -1.75). The slope on negative values alone is 0.032 with t 0.79.
- **F5:** The effect is uneven across periods and coins, which partly explains why the result is unclear. The 7-day slope inside the profile is 0.065 in 2021 (t 4.53) and 0.033 in 2020 (t 2.27), but -0.018 in 2018 and -0.020 in 2019 (t -0.51 and -1.47). By coin it is strong for XRP (0.134, t 2.53) and ETH (0.085, t 3.08), and near zero for BTC (t 0.49) and XMR (t 0.59).

## Ideas
- `077-01.b1.b1_graded-swing-rise-carries-on` (from F1, F2, F3, F5): In a choppy, calm market, a coin whose 14-day return is positive against its own daily swing over the past 30 days keeps rising over the next 7 days, and the larger that swing-scaled rise, the larger the further rise.
- `077-01.b1.b2_choppy-calm-swing-momentum` (from F1, F2, F4, F5): In a choppy, calm market, a coin's 14-day return measured against its own daily swing over the past 30 days carries on the same way over the next 7 days, and the larger that swing-scaled move up or down, the larger the further move in its direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
