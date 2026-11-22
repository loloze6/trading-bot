---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising
line: 7.b inconclusive
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The heavier that hour's volume against its 30-day average and the larger its rise against its typical hourly move, the larger the further rise.
Consequence: A trader would buy after a sharp high-volume hourly rise and refuse to buy into a sharp high-volume hourly drop, since only the rise is followed by a one-day move several times the cost of a trade.
Why:
- F1: The tested idea comes out on its predicted side but well short of the bar: recomputed over 4,485 cases, the mean unusual 24-hour move is +0.059 % with t 0.94 (step 5: +0.066 %, t 1.03, 4,448 cases), a strength of only 0.016 of the coin's usual 4.12 % daily move, and about 0.6 times the 0.11 % cost of a trade.
- F2: The effect is mixed across periods rather than steady. The mean unusual 24-hour move is +0.50 % (t 2.71, 580 cases) in 2020 and +0.35 % (t 1.75, 609 cases) in 2021, but −0.38 % (t −1.57, 553 cases) in 2018 and −0.28 % (t −1.93, 540 cases) in 2025, and only 54 % of the 24 windows have a positive mean, with a spread of 0.45 % between windows.
- F5: Recomputed from prices, hourly rises of at least 3 of their 30-day standard deviations show the clearest continuation on volume of 3 to 6 times the 30-day average: +0.68 % over 24 hours (t 2.80, 309 cases). The same rises on volume above 6 times average give +0.44 % (t 1.32, 170 cases), and on volume of 1.5 to 3 times average +0.16 % (t 0.45, 188 cases). At 6 hours the 3-to-6-times group gives +0.24 % (t 1.80, 407 cases).
