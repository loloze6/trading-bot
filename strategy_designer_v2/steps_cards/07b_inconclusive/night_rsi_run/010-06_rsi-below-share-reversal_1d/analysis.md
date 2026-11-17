---
line: 7.b inconclusive
backtest: 010-06_rsi-below-share-reversal_1d
idea tested: 010-06_rsi-below-share-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2412 USD
---
## Findings
- **F1:** The tested slope is on the side opposite to the idea, not a weak positive. At 14 days it is -0.00118 (t -1.65, 373 cases), it is negative at every horizon tried (3 days -0.00031, t -2.33, n 1856; 7 days -0.00062, t -1.85, n 799; 28 days -0.00192, t -1.26, n 187), and the book's timing gain is also negative (-0.00103 a day). More time below 50 was followed by slightly lower returns, not the higher returns the idea forecasts.
- **F2:** The negative slope does not hold across time. At 14 days, 6 of 8 years have a positive slope (2018 +0.0018, 2020 +0.0024, 2021 to 2024 between +0.0003 and +0.0011, all with |t| < 1.1), and the pooled negative comes from 2019 (-0.0041, t -1.55) and 2025 (-0.0023, t -1.76). At 28 days, 2019 (t -2.32) and 2020 (t +2.18) point in opposite directions.
- **F3:** The effect is not graded in the forecast. At 14 days the coin-demeaned return by forecast quintile runs +0.032 (t 1.51), +0.008, -0.009, -0.049 (t -2.81), +0.011 (t 0.53), so the largest forecasts do not carry the largest moves. The 3-day and 7-day quintiles show the same hump at the fourth quintile (-0.0063, t -1.82; -0.0130, t -1.54).
- **F4:** No coin, side or trend regime holds the effect clearly.

## Ideas
- No ideas: The result is on the side opposite to the idea, and the opposite (momentum) reading is not clear either. It comes from two years out of eight, is not graded across the forecast's quintiles, and shows clearly on no coin, side or regime, so no part of the data shows an effect that an amended idea could rest on.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
