---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h
instruments: BTC, ETH, LTC, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday move is followed over the next 48 hours by a move in the same direction, the larger the heavier its weekend volume is against its mean over the preceding five weekdays, whatever the size of the weekend move itself.
Consequence: After a weekend, the weekend-to-weekday volume ratio, not the size of the move, is the reason to follow the move into Monday and Tuesday and to size that bet.
Why:
- F1: On weekends ending Sunday 23:00 UTC, the signed 48-hour move after the weekend (in usual 48-hour moves) grows with the log of the weekend-to-weekday volume ratio, with slope 0.187 and t 4.48 over 1904 cases. Windows ending on other weekdays show slopes of 0.015–0.064 with t of 1.8 or less, so the volume grading is specific to the weekend. By coin it holds in XRP (t 3.77), BTC (t 2.63), ETH (t 2.52) and LTC (t 1.93), but not in ZEC (t 0.18).
- F2: Inside heavy weekends (ratio above 1), the continuation does not grow with the size of the move: the slope on |move| is −0.070 with t −0.91 over 349 cases. The idea's size check failed because it graded by move size, not by volume (the size check came out at −0.0025). The volume ratio is what carries the effect.
- F3: The top volume-ratio quintile continues on both sides. Weekend rises go on by +0.257 usual moves over 48 hours (t 2.80, n 223) and weekend falls by +0.218 (t 2.34, n 158). The middle three quintiles sit near 0 (−0.012 to +0.095).
