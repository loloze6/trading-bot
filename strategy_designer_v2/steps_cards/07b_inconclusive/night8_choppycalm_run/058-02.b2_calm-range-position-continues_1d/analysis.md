---
line: 7.b inconclusive
backtest: 058-02.b2_calm-range-position-continues_1d
idea tested: 058-02.b2_calm-range-position-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2143 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar: slope +0.000288 with day-clustered t 0.73 (567 grid cases, 282 days). Its size is also positive and uncertain: an unusual move of +0.42 % per case over 5 days, t 1.25 over 588 days, a strength of 0.044.
- **F2:** On folds B and C alone, the same regression gives slope +0.00145 with t 1.90 on 201 cases. The full-period t of 0.73 therefore means the 366 cases of folds A and D carry a weaker effect: the sign holds, but its strength changes from period to period.
- **F3:** The effect is mixed across periods. By window, w12 has slope +0.0055 (t 1.99) while w7 has −0.0044 (t −2.83), and most others are near zero (w8 t −0.01, w10 t 0.01, w14 t −0.04). By year, 2021 has t 2.94 on 34 cases, against 2018 t −1.21 and 2019 t −0.11.
- **F4:** The effect is mixed across coins too: XRP t 2.11 (40 cases), ZEC t 1.70 (18) and XMR t 1.38 (39) are positive, while BTC t 0.56, ETH t −0.24 and LTC t −0.28 are flat. Each coin has only 18 to 53 cases in folds B and C.
- **F5:** The grading is roughly on the predicted side, but noisy at these counts. The top two forecast quintiles are followed by +1.46 % excess over 5 days and the bottom one by −1.42 %, yet the middle quintile (−2.40 %) is lower than the bottom one, with only about 40 cases per quintile. In the signal's direction, shorts earn +2.26 % (99 cases) and longs +0.82 % (102).
- **F6:** The same positive slope shows at every horizon from 1 to 20 days, with t 2.70 at 1 day, 2.16 at 3, 1.90 at 5, 2.29 at 10 and 1.87 at 20 (186 to 201 cases). Changing the horizon would not change the answer; what is short is the number of cases.

## Ideas
- `058-02.b2.b1_calm-range-continuation-more-coins` (from F1, F2, F4, F5, F6): In a choppy, calm market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
