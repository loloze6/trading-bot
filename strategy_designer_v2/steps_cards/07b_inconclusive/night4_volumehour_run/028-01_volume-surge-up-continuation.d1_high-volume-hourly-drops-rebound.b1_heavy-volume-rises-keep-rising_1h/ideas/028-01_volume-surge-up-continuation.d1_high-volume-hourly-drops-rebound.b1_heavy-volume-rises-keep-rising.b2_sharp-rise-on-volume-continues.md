---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising
line: 7.b inconclusive
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The larger that hour's rise against its typical 30-day hourly move, the larger the further rise.
Consequence: A trader would buy after a sharp hourly rise on heavy volume and hold it for a day, and would not treat a sharp heavy-volume drop as a reason to sell short.
Why:
- F4: The forecast's grading does not sort the outcomes. By forecast quartile the 24-hour unusual move is +0.11 % (q1), −0.055 % (q2), +0.15 % (q3) and +0.034 % (q4), and more than half the cases sit at the cap of 20 (q3 mean 19.3, all of q4), so the top-against-bottom check passes on a near-flat profile.
- F5: Recomputed from prices, hourly rises of at least 3 of their 30-day standard deviations show the clearest continuation on volume of 3 to 6 times the 30-day average: +0.68 % over 24 hours (t 2.80, 309 cases). The same rises on volume above 6 times average give +0.44 % (t 1.32, 170 cases), and on volume of 1.5 to 3 times average +0.16 % (t 0.45, 188 cases). At 6 hours the 3-to-6-times group gives +0.24 % (t 1.80, 407 cases).
- F6: The same-sized hourly drops are not followed by further falls over 24 hours. On volume above 6 times average they give −0.64 % in their own direction (t −1.40, 214 cases), which is a partial rebound, so the continuation shows only on the rising side.
