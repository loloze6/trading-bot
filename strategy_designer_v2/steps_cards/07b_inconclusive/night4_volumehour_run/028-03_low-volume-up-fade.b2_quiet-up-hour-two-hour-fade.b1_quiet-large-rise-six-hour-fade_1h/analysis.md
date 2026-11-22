---
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h
idea tested: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5472 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but far below the bar: the mean short-signed unusual 6-hour move is +0.02 % per case with t 0.91 over 9,180 cases, a strength of only 0.009 of the coin's usual 6-hour move of 1.98 %. My rebuild of the signals gives the same picture at every horizon, all positive and none reaching t 2: 1 hour +0.011 % (t 1.41, 10,574 cases), 3 hours +0.019 % (t 1.35), 6 hours +0.023 % (t 1.06, 8,730 cases), 12 hours +0.038 % (t 1.12, 6,785 cases).
- **F2:** The giveback is not graded by the size of the rise, which is the second reason the result is unclear: the larger-forecast half minus the smaller half is -0.026 %. By scaled rise, the 6-hour fade is +0.029 % in (1,2] (t 1.03, 5,283 cases), -0.029 % in (2,3] (t -0.58, 1,727), and +0.138 % in (3,5] (t 1.39, 519). On the first quiet rise of each cell, the slope of the fade on the log of the scaled rise has t 1.09 at 6 hours (4,952 cases), 1.36 at 2 hours and 0.32 at 12 hours.
- **F3:** The effect does not sit in one part of the data that an amended idea could isolate. Both coins show the same sign, BTC +0.009 % (t 0.36, 4,433 cases) and ETH +0.037 % (t 1.07, 4,297). The years alternate sign with no lasting regime: 2018 +0.146 % (t 1.81), 2025 +0.104 % (t 2.01), 2020 -0.098 % (t -1.60), 2023 -0.049 % (t -1.20), 2024 -0.002 % (t -0.04).
- **F4:** The effect is drowned by the market's own moves rather than absent. A +0.02 % mean against a usual move of 1.98 % gives t 0.91 on 9,180 cases. At the same mean, reaching t 2 would need about (2/0.91)² ≈ 4.8 times as many cases, which BTC and ETH alone cannot supply, since the test already used all four folds.
- **F5:** The quiet-volume reversal is just as faint on the other side: the first quiet-volume fall of at least 2 usual moves in each 6-hour cell is followed by a bounce of +0.050 % (t 1.08, 2,332 cases). There is no stronger one-sided version of the idea to narrow to.

## Ideas
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade.b1_quiet-rise-fade-more-coins` (from F1, F3, F4): After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next six hours. The larger that hour's rise in multiples of its typical move, the larger the giveback, most of all for rises several times the typical move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
