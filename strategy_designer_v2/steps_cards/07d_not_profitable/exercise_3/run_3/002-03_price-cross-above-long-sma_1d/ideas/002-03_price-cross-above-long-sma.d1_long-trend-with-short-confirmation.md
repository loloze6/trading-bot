---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When the coin's close is above its 200-day moving average, price keeps rising over the following bars, and further the farther the close sits above it. This holds only while the close also sits above its short moving average, and the rise is larger the farther above that short average the close sits.
Consequence: A trader stays long above the long average only while the short-term trend also points up, and steps aside when the close slips back to its short average, which is when the falls happen.
Why:
- F1: The book fails on its falls. Its deepest fall over the daily returns chained in window order is -43.0 % against a yearly return of 16.6 % (Calmar 0.3855, needed 0.75). That fall is one episode across w15 to w17, where the reconstructed book lost 18.8 %, 8.4 % and 21.6 % over 67, 120 and 22 days.
- F2: Inside that episode every coin lost money for the book (summed gains -0.38 to -0.65). Each coin stood far below its 60-day high (mean dd60 -0.24 to -0.41) with its close at or below its 20-day SMA (mean distance 0.000 to -0.043). Its close was still mostly above the 200-day SMA (mean distance -8 to +21 %), so the forecast kept the book long through a short-term decline.
- F3: The long position earns only while the coin is in a short-term uptrend. With the close 0.0355 to 0.105 above its 20-day SMA, the mean bar gain is 0.00159 (t 2.23, n 1649), and above 0.105 it is 0.00368 (t 3.20, n 1650). With the close between -5.8 % and +3.6 % of that SMA, the mean gain is about zero (-0.00021 with t -0.39, and 0.00014 with t 0.24).
- F5: Gains also turn negative after a down month. In the lowest quintile of the past 20-bar return (below -9.7 %) the mean bar gain is -0.00022 (t -0.76, n 1635), against 0.00225 to 0.00254 (t 2.80 and 2.25) in the top two quintiles.
- F6: Holding the long only while the close is above its 20-day SMA cuts the deepest fall from -42.6 % to -27.2 %. The yearly return stays about the same (0.174 against 0.178), so Calmar rises from 0.418 to 0.640. Holding only after a positive past 20 bars gives a deepest fall of -30.0 %, a yearly return of 0.185 and Calmar 0.616.
