---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each day, the coin rises over the four hours after 21:00 UTC by more than over its other four-hour stretches, and the rise is larger the higher its realised hourly volatility over the past 7 days, only while that 7-day volatility stands in the upper part of its own range over the past several weeks.
Consequence: A trader would take the evening long only on the coin's most volatile evenings and give it full weight there, where the move is about 28 bps against a 19 bps round trip, instead of scaling it down.
Why:
- F1: The evening move is smaller than the cost of a trade. Over the 4 hours from the 21:00 UTC close, the coins rise 10.8 bps on average, against 19 bps for a buy and a sell. On the book itself, the four evening hours earn about 4.9 bps per coin-day (1.96, 2.46, -0.70 and 1.15 bps on hours 20 to 23), while the fees at the open and the close of the bet cost about 8.6 bps (4.39 and 4.25 bps). The book earns 0.21 bps per bar and pays 0.37 bps.
- F2: The evening rise is almost all in the coin's most volatile fifth of evenings. There the 4-hour unusual move is +27.8 bps (total +30.1 bps), against +0.3 to +5.3 bps in the four other fifths (about 3,365 evenings each).
- F3: The volatility sizing undoes the idea's grading. The position held is 0.38 in the most volatile fifth of evenings against 0.60 in the calmest. The book's 4-hour evening gain therefore covers its fees only in the top fifth (11.8 bps of gain against 6.7 bps of fees). In the other four fifths it earns 1.1 to 5.2 bps against 7.9 to 11.1 bps of fees.
