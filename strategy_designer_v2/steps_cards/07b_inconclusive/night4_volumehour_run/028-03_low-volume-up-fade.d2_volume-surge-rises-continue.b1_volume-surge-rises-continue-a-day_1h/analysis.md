---
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day_1h
idea tested: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 0
cost: 0.1663 USD
---
## Findings
- **F1:** The test's own measure, rebuilt case by case, is on the side the idea predicts but small. It is a mean strength of +0.0156 with t 1.02 over 4,448 cases, which is +0.07 % per case against a usual 24-hour move of 4.12 %. At that strength, about 17,000 cases would be needed to reach t 2, roughly four times what BTC and ETH give over folds A to D.
- **F2:** The effect is not hidden at another horizon. The mean strength is positive and of about the same size at every horizon: +0.010 over 2 hours (t 0.69), +0.013 over 6 hours (t 0.86), +0.014 over 12 hours (t 0.97), +0.016 over 24 hours (t 1.02) and +0.011 over 48 hours (t 0.74), with 4,446 to 4,448 cases each.
- **F3:** The grading the idea claims shows in order but is not significant anywhere. Across forecast quintiles, the 24-hour strength rises steadily from -0.010 (t -0.29) in the lowest fifth to +0.039 (t 1.15) in the highest, about 890 cases each. Across volume-ratio quintiles, the 6-hour strength rises from -0.005 (t -0.16) to +0.036 (t 1.07). No part of the data shows the effect clearly while it is absent elsewhere.
- **F4:** The effect is present in both coins, larger in BTC and weak in ETH. BTC has a strength of +0.025 (t 1.16, 2,224 cases) and ETH +0.006 (t 0.29, 2,224 cases). Its split by fold is not usable: the table came back with mislabelled folds.
- **F5:** The move is too small for this data to show clearly, and too small to trade. The unusual move of +0.07 % per case is 0.6 times the 0.11 % cost of a trade. The book's Sharpe of 0.58 trails holding the coins by 0.058.

## Ideas
- `028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day.b1_volume-surge-rises-more-coins` (from F1, F2, F3, F4): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The higher that hour's volume against its 30-day average, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
