---
line: 7.b inconclusive
backtest: 058-03.g1.b1_calm-downtrend-weekly-continuation-more-coins_1d
idea tested: 058-03.g1.b1_calm-downtrend-weekly-continuation-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3513 USD
---
## Findings
- **F1:** Over 5 days, the test's slope is on the predicted side but small: the full test gave a slope of +0.0043 per forecast/10 with a day-clustered t of 0.90 (1274 grid cases, 309 days). On folds B and C alone it gives +0.0147 with t 1.78 (427 cases, 137 days). The per-case size points the same way: an unusual move of +0.80 % with t 2.13 over 746 days. Since every fold and every coin was already used, more data is not the answer.
- **F2:** The continuation is stronger over a shorter horizon. Inside the falling calm profile on folds B and C, the slope of the excess return on the forecast has:
- **F3:** The effect lives in the falling calm profile only. Outside it, the past 5-day return predicts nothing over 5 days (slope t -0.07 on 1258 cases), and the next-5-day excess return is flat across past-return quintiles (+0.6 %, -0.9 %, +0.6 %, +1.1 %, +0.6 %). Inside the profile the same 3-day slope has t 2.69.
- **F4:** Inside the profile the effect leans to the falling side:
- **F5:** The effect varies by year:

## Ideas
- `058-03.g1.b1.b1_calm-downtrend-three-day-continuation` (from F2, F3, F1): In a falling, calm market, a coin's last 5 days carry on over the next 3 days: the further it has fallen over its last 5 days, the more it falls over the next 3 days, and the further it has risen over those 5 days, the more it rises.
- `058-03.g1.b1.b2_calm-downtrend-falls-continue` (from F4, F2, F3): In a falling, calm market, a coin's fall over its last 5 days carries on: the further it has fallen over its last 5 days, the more it keeps falling over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
