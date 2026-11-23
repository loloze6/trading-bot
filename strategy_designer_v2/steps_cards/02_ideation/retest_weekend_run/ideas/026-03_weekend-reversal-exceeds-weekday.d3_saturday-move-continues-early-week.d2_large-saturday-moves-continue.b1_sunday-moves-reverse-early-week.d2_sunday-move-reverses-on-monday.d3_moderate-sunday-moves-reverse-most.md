---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday, measured against its usual 30-day move, is followed over the next 48 hours by an opposite move that grows with the product of that scaled Sunday move, up to about two usual moves, and the coin's 30-day hourly volatility.
Consequence: A trader would size the lean against Sunday's move by its size times the coin's hourly volatility, and not let the most extreme Sundays take the largest stake.
Why:
- F1: The book sizes against its own effect: the vol-target sizing holds a mean position of 0.56 on Mondays in the lowest pooled tercile of 30-day hourly volatility, where the reversal is nil (-0.004 %, t -0.03, n 604; position-weighted -0.17 %), but only 0.21 on the highest tercile, where the reversal is +0.98 % per case (t 3.27, n 604); the middle tercile gives +0.56 % (t 3.06) at a position of 0.36.
- F4: High volatility is not an effect of its own. On other days of the week, a day's 24-hour move is reversed over the next 24 hours by only +0.12 % (t 1.75, n 7281) in the highest volatility tercile, against +0.98 % after a Sunday at the same volatility. Monday's reversal at high volatility is not a general drift either: Monday's unsigned excess move is -0.23 % (t -0.77). The volatility grading is the idea's own stated condition.
- F6: The reversal keeps going into Tuesday. Over 48 hours it is +0.58 % per case (t 3.82, n 2404) against +0.39 % over 24 hours (t 3.61), with hours 24–48 alone adding +0.21 % (t 2.19). In the highest volatility tercile it grows from +0.98 % to +1.37 % (t 3.49), and in the middle one from +0.56 % to +0.99 % (t 4.09).
- F8: Sunday's largest moves are not reversed more. The top fifth by size of Sunday's move in usual moves (mean 2.2) reverses +0.22 % (t 0.70), against +0.55 % to +0.67 % in the other four fifths, yet the book gives that fifth its largest position (0.83).
