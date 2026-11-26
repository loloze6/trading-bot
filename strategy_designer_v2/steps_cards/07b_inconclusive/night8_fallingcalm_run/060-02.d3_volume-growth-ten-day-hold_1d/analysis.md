---
line: 7.b inconclusive
backtest: 060-02.d3_volume-growth-ten-day-hold_1d
idea tested: 060-02.d3_volume-growth-ten-day-hold
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1941 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar: the main measure is +0.083 with t 1.87 on 147 day-cases (447 cells), with a rank correlation of +0.165, and the idea's size is an unusual move of +2.35 % per case over 10 days (t 3.45 over 410 days, 562 cases, strength 0.156).
- **F2:** In folds B and C the 10-day measure is +0.177 with t 1.96 on only 65 day-cases, and it is positive on every one of the six coins (t from 0.20 for BTC to 2.38 for XRP, directional excess return +1.0 % to +5.7 %); the effect is spread across coins, and each coin contributes too few cases to show it alone.
- **F3:** The effect is positive in every year shown (2018 t 1.37, 2019 t 1.59, 2020 t 1.19, 2021 t 0.51) and in 9 of 11 windows; the two negative windows hold only 1 and 4 day-cases, so the effect is not confined to one period.
- **F4:** Both sides carry it: long cells (volume grew) give +0.121 (t 1.04, 41 days, directional excess +3.5 %) and short cells (volume shrank) give +0.134 (t 1.65, 49 days, +2.4 %), so the effect is not one-sided.
- **F5:** The test's horizon is not the problem: the measure is about as clear over 5 days (t 1.90, 136 day-cases) and over 20 days (t 1.55, 34 day-cases) as over 10 days (t 1.96).
- **F6:** The effect is graded as the idea says: the largest quartile of |forecast| gives a directional excess of +10.7 % on the short side (t 2.98, 18 days) and +7.0 % on the long side, while the smallest quartile is near 0 (+0.2 % long, −1.1 % short).
- **F7:** Splitting by agitation leaves only 76 cells with a known profile (calm +0.165, t 1.58; agitated +0.065, t 0.21), too few to say the effect lives in one agitation.

## Ideas
- `060-02.d3.b1_volume-growth-all-coins` (from F1, F2, F3, F4, F5, F6): In a falling market, while the coin's 20-day return is still negative, the more its trading volume over the past 30 days has grown against the 30 days before, the smaller its fall, or the larger its rise, over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
