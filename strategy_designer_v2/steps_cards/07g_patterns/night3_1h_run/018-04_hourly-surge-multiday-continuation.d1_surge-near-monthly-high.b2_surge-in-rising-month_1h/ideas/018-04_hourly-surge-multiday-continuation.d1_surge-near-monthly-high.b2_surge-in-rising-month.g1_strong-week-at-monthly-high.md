---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The closer a coin's hourly close is to its highest close of the last 30 days, the more it rises over the next 10 days above its usual 10-day return, and the more so the larger its 7-day return.
Consequence: A trader would hold a coin for about ten days when it trades at its monthly high after a strong week, and refuse long entries in coins far below their monthly high after a weak week.
Why:
- F2: Nearness to the 30-day high carries a 10-day move the surge does not explain: on the grid starting at each window's first row, cells in each coin's top quintile of close over its 30-day highest close are followed by a 10-day excess return of +3.9 % (t 3.02, 278 cases), against -0.1 % to -3.0 % in the four lower quintiles; on the 5-day horizon the same top quintile gives +2.3 % (t 2.67).
- F4: Nearness and a strong 7-day return reinforce each other. Cells in both top quintiles are followed by +7.4 % excess over 10 days (t 2.97, 130 cases), against +0.8 % (t 0.83, 148) for near-high alone, +0.6 % (t 0.44, 148) for a top 7-day return alone, and -1.5 % (t -3.32, 960) for neither.
- F5: The 7-day return alone sorts the next 10 days on the first grid: -2.1 % to -1.6 % excess in the lowest three quintiles (t about -2.1 to -2.4), +3.7 % (t 2.76, 278) in the top quintile. On the shifted grid the top quintile falls to +1.1 % (t 1.03), so it is weaker than F4.
- F9: The moves in F2 and F4 are large against a trade: a 10-day excess of +3.9 % to +7.4 % per case is 20 to 39 times the 0.19 % round-trip cost of this backtest. Size is not the obstacle; robustness across grid offsets (F3) and years (F7) is.
