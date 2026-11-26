---
line: 7.b inconclusive
backtest: 058-03.g1_calm-downtrend-weekly-continuation_1d
idea tested: 058-03.g1_calm-downtrend-weekly-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1982 USD
---
## Findings
- **F1:** The result is on the predicted side but short of the bar. Over all folds step 5 found a mean of +0.0066 with t 1.03 over 255 days, while the size measure gave an unusual move of +1.08 % per case with t 2.44 over 494 days. On the visible folds B and C, the plan's product is +0.0179 (t 1.81) and the drift-adjusted 5-day move in the signal's direction is +1.56 % (t 1.92), over 371 cases on 131 days.
- **F2:** The effect is broad, not confined to one part of the data, so it is small rather than mixed.
- **F3:** Grading by forecast size is weak. The weakest third of absolute forecasts earns +0.45 % (t 0.44), against +2.35 % (t 1.82) for the middle third and +1.89 % (t 1.28) for the strongest. This is why the forecast-weighted main measure (t 1.81 visible, 1.03 overall) is no surer than the unweighted move.
- **F4:** The plan's 5-day horizon is where the effect shows best. The move in the signal's direction is −0.01 % at 1 day (t −0.03), +0.45 % at 3 days (t 0.79), +1.56 % at 5 days (t 1.92) and +1.37 % at 10 days (t 1.13). Another horizon would not sharpen it.
- **F5:** The 5-day volume against its 60-day mean does not separate the cases:

## Ideas
- `058-03.g1.b1_calm-downtrend-weekly-continuation-more-coins` (from F1, F2, F4): In a falling, calm market, a coin's last 5 days carry on over the next 5 days, and the further it has fallen over its last 5 days, the more it falls over the next 5 days. The further it has risen over those 5 days, the more it rises.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
