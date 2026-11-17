---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Monday-and-Tuesday return runs against its Sunday close-to-close move when that move is large against the coin's 20-day usual daily move, but not the very largest. Within that range, the larger the Sunday move in usual daily moves, the larger the move back over the next 2 days.
Consequence: A trader would fade ordinary-to-large weekend moves into Monday, and would not fade the most extreme weekend moves, which tend to hold.
Why:
- F1: The reversal belongs to Sunday alone: the signed 2-day move against the day's own move is 0.0082 (t 5.08, n 2051) after Sunday, while every other weekday lies between −0.0036 and +0.0008. Sunday minus the other days is 0.0079, 0.0151 and 0.0084 (Welch t 2.44, 4.78, 2.60) in the three lower |move| quartiles.
- F2: The effect is not graded at the top, which is why the supporting check failed. By |forecast| quartile, the signed 2-day reversal is 0.0037, 0.0152, 0.0125 and 0.0016 (616 cases each). In the largest |move| quartile, Sunday minus the other days is only 0.0011 (t 0.26). The median-split difference of −0.00084 is small next to these swings.
- F3: In the middle quartiles both sides reverse. After a fall the signed reversal is 0.0109 and 0.0092 (t 2.60, 2.05); after a rise it is 0.0163 and 0.0104 (t 3.94, 2.55). In the largest quartile neither side reverses (fall 0.0032 with t 0.49, rise −0.0012 with t −0.22).
- F5: Most of the reversal shows on Monday, and it does not decay afterwards. The signed reversal is 0.0056 (t 4.71) over 1 day, 0.0082 (t 5.08) over 2 days, 0.0086 over 3 days and 0.0087 over 5 days. Tuesday alone adds 0.0029 (t 2.79).
