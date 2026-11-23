---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the next 24 hours after a fall over a coin's last 2 hours, at any hour of the day, runs upward, only once the fall is among the coin's deepest 2-hour falls against its usual 2-hour move, and the deeper the fall within those, the larger the rise.
Consequence: A trader stays out of the coin except after its deepest 2-hour falls, so the book stops carrying the coin's crashes and keeps the rebound that covers a trade's cost several times over.
Why:
- F1: The book was in fact always long, whatever the signal: the position after a trade was above 0.01 on 99.9 % of bars (mean allocation 0.93, median 0.87), and its days in a position were 100 %. Its daily returns had a 0.94 correlation with holding the coins, and its deepest fall was -67 % against holding's -81 %. So the failed Calmar (0.38) is the coins' own crashes carried by a near-permanent long, not the idea losing money. Windows w2, w14 and w16 fell -53 %, -55 % and -57 % inside the window.
- F2: The effect sits only in the deepest falls. Over 24 hours on the non-overlapping grid, the forecast quintiles 1 to 4 earn an excess of 0.00 %, +0.02 %, +0.02 % and +0.09 % (all t < 0.9, about 1,740 cases each). The top quintile (forecast ≥ 15.7) earns +0.60 % excess (t 4.29, 1,742 cases), and the 1,138 cases at the cap of 20 earn +0.71 % (t 3.84). This is why the idea's size over all 17,241 cases is only +0.01 % unusual move.
- F3: For the top quintile, the total move over 24 hours is +0.75 % per case, about 4 times the 0.19 % cost of a trade. After that cost it nets +0.56 % per case (t 3.96), with 57.5 % of cases rising.
- F4: An approximate book that is long only on top-quintile grid cells and pays 0.19 % per trade had these results: in the market 10 % of the time, a yearly return of +19.4 %, a deepest fall of -21 % (Calmar about 0.92, against 0.75 required) and a Sharpe of 0.86. Holding on the same grid gave +29 % a year with a deepest fall of -76 %.
