---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month
line: 7.b inconclusive
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 10 days by more than the coin's usual 10-day return, only while that close is near the coin's 30-day high: the nearer the close to the 30-day high and the larger the surge in usual daily moves, the larger the rise.
Consequence: A trader would hold an hourly-caught surge for about ten days when it lifts the price to the top of its monthly range, and refuse surges that leave the price well below its 30-day high.
Why:
- F2: Most of the effect sits in the largest surges. The 359 cases where the forecast is at its cap of 20 gain +2.2 % over 10 days beyond drift (t 2.13). The 797 cases below the cap gain −0.2 % (t −0.40). By forecast quartile the excess climbs from −0.65 % to −0.40 %, +0.83 % and +2.38 % (t 1.91 in the top quartile).
- F3: The effect also sits in surges that end near the 30-day high. Cases within about 1 % of the 30-day high (top quartile, median 1.0 % below it) gain +4.6 % over 10 days beyond drift (t 2.86, 214 cases). The other three quartiles gain −0.1 %, −1.9 % and +0.9 %.
- F7: The move is not too small to pay, but the book's falls are deep. The unusual move per case is 3.0 times the 0.19 % cost of a round trip, and the total move is 10.1 times it. The book's Sharpe is 0.82, above holding by 0.27, but it fails on Calmar (0.62), consistent with the losing years in F4.
