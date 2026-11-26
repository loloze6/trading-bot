---
line: 7.b inconclusive
backtest: 032-03_low-volume-decline-continues-more_1d
idea tested: 032-03_low-volume-decline-continues-more
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3376 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but far from the bar: the slope of the 5-day excess return on the forecast is +0.00022 with a day-clustered t of 0.48 (1,616 regime cells on 468 days, 944 cells with forecast ≤ -2). On folds B and C, the slope on the raw log volume ratio is also positive but unclear (+0.0118, clustered t 1.06, 741 cells on 217 days; on the forecast +0.00049, t 0.58).
- **F2:** The effect is mixed across periods and coins. Window slopes run from -0.100 (t -3.43, w17) to +0.126 (t 2.47, w13). By year only 2018 shows it (slope +0.033, t 2.51, n 209); 2019 to 2021 are near 0 (t -0.03, -0.65, +0.04). By coin, BTC, ETH, LTC and XMR have positive slopes (t 1.95, 0.87, 1.56, 1.41), while XRP and ZEC have negative ones (t -0.98, -0.21). Six coins on this data cannot separate the effect from this noise.
- **F3:** The contrast between thin and heavy volume sits mostly at the heavy end, which the forecast's clip at 0 sets flat. The 5-day excess return by volume quartile is -0.83 %, -1.47 %, -0.99 % for the three thinner quartiles and +1.22 % for the heaviest. Cells with the ratio below usual average -0.90 % (462), against +0.11 % (279) at or above usual. Inside the forecast's own range (ratio < 0), the slope is weak (clustered t 0.59; the raw ratio and the forecast correlate at 0.86 there).
- **F4:** The 28-day decline itself is followed by further falls that grow with the horizon. The mean excess return after declines is -0.71 % over 5 days (554 cells), -1.11 % over 10 days (273) and -1.81 % over 20 days (125). Outside declines it is +0.39 %, +0.60 % and +0.88 %.
- **F5:** Declines that are both deep and thin fall most: -2.42 % over 5 days (111 cells), against -0.31 % for deep with heavy volume, -0.60 % for shallow with thin volume and +0.46 % for shallow with heavy volume. Over 10 days, a deeper 28-day fall is followed by a larger excess fall (slope on the 28-day return +0.133, t 1.97, n 273, not clustered). Over 5 days that link is absent (t -0.15), and the clustered interaction of depth and volume is not significant (t -0.81).
- **F6:** The book cannot pay at this size. The idea's unusual move per case is -0.51 % (t -1.17, 495 days, strength -0.043) and the total move is -1.17 %, which is -6.1 times the 0.19 % cost of a trade. The book's Sharpe is -0.15 and its yearly return -4.5 %.

## Ideas
- `032-03.b1_thin-volume-decline-more-coins` (from F1, F2, F3): Among coins that have fallen over the past 28 days, the lower the volume over that period compared with the coin's own usual volume, the larger the further fall over the next 5 days.
- `032-03.b2_deep-calm-decline-continues` (from F4, F5): Among coins whose volume over the past 28 days is below their own usual volume, the larger the fall over those 28 days, the larger the further fall over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
