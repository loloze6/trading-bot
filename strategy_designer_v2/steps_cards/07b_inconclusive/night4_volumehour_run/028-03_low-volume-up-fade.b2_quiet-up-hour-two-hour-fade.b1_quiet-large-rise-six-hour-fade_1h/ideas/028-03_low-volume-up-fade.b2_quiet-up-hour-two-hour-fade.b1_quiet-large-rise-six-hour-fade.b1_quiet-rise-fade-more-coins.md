---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next six hours. The larger that hour's rise in multiples of its typical move, the larger the giveback, most of all for rises several times the typical move.
Consequence: A trader would refuse to chase, or would fade, a quiet-volume hourly rise several times its usual size for the following six hours, since its giveback grows with the size of the rise.
Why:
- F1: The test's result is on the side the idea predicts but far below the bar: the mean short-signed unusual 6-hour move is +0.02 % per case with t 0.91 over 9,180 cases, a strength of only 0.009 of the coin's usual 6-hour move of 1.98 %. My rebuild of the signals gives the same picture at every horizon, all positive and none reaching t 2: 1 hour +0.011 % (t 1.41, 10,574 cases), 3 hours +0.019 % (t 1.35), 6 hours +0.023 % (t 1.06, 8,730 cases), 12 hours +0.038 % (t 1.12, 6,785 cases).
- F3: The effect does not sit in one part of the data that an amended idea could isolate. Both coins show the same sign, BTC +0.009 % (t 0.36, 4,433 cases) and ETH +0.037 % (t 1.07, 4,297). The years alternate sign with no lasting regime: 2018 +0.146 % (t 1.81), 2025 +0.104 % (t 2.01), 2020 -0.098 % (t -1.60), 2023 -0.049 % (t -1.20), 2024 -0.002 % (t -0.04).
- F4: The effect is drowned by the market's own moves rather than absent. A +0.02 % mean against a usual move of 1.98 % gives t 0.91 on 9,180 cases. At the same mean, reaching t 2 would need about (2/0.91)² ≈ 4.8 times as many cases, which BTC and ETH alone cannot supply, since the test already used all four folds.
