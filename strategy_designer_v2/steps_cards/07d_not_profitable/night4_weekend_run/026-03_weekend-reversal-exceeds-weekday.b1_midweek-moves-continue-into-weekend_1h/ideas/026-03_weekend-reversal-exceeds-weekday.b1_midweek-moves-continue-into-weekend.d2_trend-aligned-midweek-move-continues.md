---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 48-hour return over Wednesday and Thursday is followed by a move in the same direction over the next two days, Friday and Saturday, and the larger the Wednesday-Thursday move, the larger the move that follows, only while that move goes the same way as the coin's 14-day return.
Consequence: A trader would follow a midweek move into the weekend only when it extends the coin's two-week trend, sizing by the move.
Why:
- F1: The book's whole edge per case is too thin for its cost: the 2379 Thursday-23:00 cases move +0.30 % in total over 48 hours against a 0.19 % round-trip cost, the 4130 recorded trades average −0.09 % gross and −0.19 % net, and the book is flat five days a week, so its mean daily return is only 0.011 % against 0.05 % required.
- F4: The continuation shows when the midweek move goes the same way as the coin's 14-day return: +0.61 % over 48 hours (t 3.33, 1303 cases). Against the 14-day trend it partly reverses: −0.33 % (t −1.65, 809 cases).
- F5: Among the largest 48-hour moves, only those read on Thursday's close carry the following 48-hour move: +1.08 %, t 2.97, 470 cases. Every other weekday's |t| is 1.45 or less.
