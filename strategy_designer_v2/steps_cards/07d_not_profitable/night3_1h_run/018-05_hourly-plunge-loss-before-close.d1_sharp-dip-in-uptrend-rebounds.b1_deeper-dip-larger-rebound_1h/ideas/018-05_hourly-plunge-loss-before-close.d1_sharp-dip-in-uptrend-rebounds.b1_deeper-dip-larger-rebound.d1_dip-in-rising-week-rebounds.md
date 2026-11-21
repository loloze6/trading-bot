---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound
line: 7.d not profitable
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return while its 30-day return is positive, the coin rises over the next 3 days more than its normal drift, only while its 7-day return is positive, and the higher its 7-day return, the larger the rise.
Consequence: Buy a sharp one-day drop in a month-long rise only when the past week is still up, sized up the stronger that week, and refuse dips whose week has already turned down, which is where the deep losses sit.
Why:
- F1: The check fails on Calmar alone (0.60 against 0.75). The chained book's deepest fall is −33.0 % against a yearly return of +19.9 %, and that fall runs 217 days from w1 to w3, while holding the coins lost 65.9 % over the same stretch. Book returns were −6.6 %, −13.9 % and −8.0 % in w1, w2 and w3, and its deepest falls inside one window are −23.8 % (w3), −21.9 % (w14) and −20.6 % (w18), all windows where holding lost (−10 %, −49 %, −22 %).
- F2: The dips that rebound are the ones whose week is still rising. Across 1,887 recomputed cases, the unusual 72-hour return rises steadily with the coin's 7-day return:
- F3: The dip's own depth does not grade the rebound; the 30-day and 7-day trends do.
