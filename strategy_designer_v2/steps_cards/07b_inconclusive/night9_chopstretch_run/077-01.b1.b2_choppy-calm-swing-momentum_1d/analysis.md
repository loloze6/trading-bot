---
line: 7.b inconclusive
backtest: 077-01.b1.b2_choppy-calm-swing-momentum_1d
idea tested: 077-01.b1.b2_choppy-calm-swing-momentum
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3581 USD
---
## Findings
- **F1:** Inside the choppy-calm profile, on the 7-day grid of folds B and C, the forward excess return rises with the swing-scaled 14-day move (slope 0.042, day-clustered t 2.69, 151 cases on 65 days; on the forecast 0.0023, t 2.02). Step 5's slope over all four folds is 0.00027 with t 0.35 on 777 cases. The effect seen in B and C therefore barely survives in folds A and D. The full test's result is on the predicted side but close to zero.
- **F2:** The test already used every fold and every coin on daily bars. More 1d data is not available. A finer bar does not add independent 7-day cases either.
- **F3:** Inside the profile the carry is driven by the largest moves, and above all by the largest rises:
- **F4:** The falling side does not carry in a graded way:
- **F5:** The effect is uneven in time. Only 2021 is clearly positive (+5.4 % per case, t 2.77, n 51). Window w18 alone gives +15.9 % (t 3.41, n 13). 2019 is -0.1 % (t -0.06), and w7/w8 are slightly negative. This explains why the effect drowns in the folds not shown.
- **F6:** The horizon is not the cause:
- **F7:** Outside the profile the carry is weaker per unit of move than inside (clustered slope 0.0128, t 1.39, 994 cases, against 0.042 inside). It is still graded across |z| quartiles, from +1.0 % to +2.8 % (top quartile t 2.45). The choppy-calm profile concentrates the effect but is not its only home.

## Ideas
- `077-01.b1.b2.b1_choppy-calm-large-rises-carry` (from F1, F3, F4, F6): In a choppy, calm market, a coin whose 14-day rise, measured against its own daily swing over the past 30 days, is large keeps rising over the next 7 days, and the larger that swing-scaled rise, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
