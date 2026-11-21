---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds
line: 7.b inconclusive
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return while its 30-day return is positive, the coin rises over the next 3 days more than its normal drift, and the deeper the 24-hour fall in multiples of its 30-day average absolute daily return, the larger the rise.
Consequence: A sharp one-day drop inside a month-long rise is a reason to buy for a few days, sized up the deeper the drop is relative to the coin's usual daily move.
Why:
- F1: The test's mean is on the predicted side and past the bar: +0.49 % unusual move over 72 hours, t 2.99, on 2803 cases. The verdict is inconclusive only because the forecast's cap made the supporting check impossible: 54 % of cases (1515 of 2803) entered at exactly +20, so the median entry forecast is 20 and no case lies above it (0 above, 2803 at or below).
- F2: Within the cases, the size of the forecast does not grade the move. On the raw component, cases above the median minus those below differ by +0.09 %, Welch t 0.26 (1401 vs 1402 cases). Its quintiles are U-shaped: +0.72 %, +0.12 %, +0.18 %, +0.64 %, +0.81 %.
- F3: The 30-day rise does not grade the rebound either. On the 72-hour grid, dips (24-hour fall above 0) inside a positive month show no ordering across quintiles of the 30-day return in usual 30-day moves: +0.27 %, -0.31 %, +1.57 %, +0.24 %, +0.55 % (190 cases each).
- F4: What grades the rebound is the depth of the 24-hour fall. On the 72-hour grid with a positive 30-day return, falls of 0.5 to 1, 1 to 1.5 and over 1.5 times the 30-day mean absolute daily return are followed by +0.67 % (t 1.29, n 259), +0.87 % (t 1.42, n 164) and +2.67 % (t 3.58, n 171). The product of fall and rise ranks with the move at Spearman rho 0.13 (p 4e-5, n 950).
- F7: The move carried over 72 hours is large next to the 0.19 % cost of a round trip. The total move is 0.90 % per case (4.7 times the cost), and 2.67 % unusual on the deepest falls. The book paid: Sharpe 1.11, 0.56 above holding.
