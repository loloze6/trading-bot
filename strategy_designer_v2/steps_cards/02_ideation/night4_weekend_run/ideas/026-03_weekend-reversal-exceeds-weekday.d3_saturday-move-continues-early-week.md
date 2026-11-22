---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Saturday is followed over the next two days by a move in the same direction, and the larger Saturday's move, the larger that continuation.
Consequence: A trader would follow Saturday's move into Monday and Tuesday instead of fading it, the side the current book loses on.
Why:
- F2: The 48-hour weekend return joins two halves that act in opposite ways. Across 2387 Monday-00:00 cases, Saturday's 24-hour return correlates +0.071 with the next 48 hours (t 3.47), while Sunday's correlates -0.083 (t -4.06). The full 48-hour return the book trades on correlates only -0.013 (t -0.62), so the two halves cancel.
- F5: Saturday's move continues: at Monday 00:00, the next 48 hours in the direction of Saturday's 24-hour return average +0.45 % unusual move (t 2.99, 2387 cases).
