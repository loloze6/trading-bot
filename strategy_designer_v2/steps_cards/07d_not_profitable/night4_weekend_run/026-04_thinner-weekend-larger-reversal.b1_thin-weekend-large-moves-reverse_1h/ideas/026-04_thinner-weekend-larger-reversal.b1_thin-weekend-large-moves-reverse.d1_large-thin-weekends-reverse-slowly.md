---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday move is partly reversed over the next 96 hours (Monday to Thursday), only while its weekend volume is lower than its mean volume over the preceding five weekdays. The share reversed rises steeply with the size of the weekend move counted in the coin's usual 2-day moves, so the largest weekend moves carry most of the reversal, and it grows the lower the weekend volume is against the weekdays.
Consequence: A trader leans against only the weekend moves that are large next to the coin's usual 2-day move and holds into Thursday, and refuses the trade after a modest weekend move, which tends to continue.
Why:
- F1: The book trades every thin weekend, whatever the size of its move, and the small moves continue instead of reversing. On thin Sunday-23:00 cases, the two quintiles with the smallest absolute weekend move have an unusual 48 h move of -0.65 % (t -2.26, n 379) and -0.81 % (t -2.36, n 378). Only the largest-move quintile reverses, by +1.02 % (t 2.36, n 378), which is about 5 times the 0.19 % trade cost; pooled, the idea's size is 0.002 of a usual move.
- F2: The reversal on thin weekends is slow. The slope of the forward return on the weekend move (in usual moves) is -0.030 (t -1.51) at 12 h, -0.067 (t -1.72) at 48 h and -0.173 (t -3.27, n 1812) at 96 h. For the largest-move quintile the unusual move rises from +1.02 % at 48 h to +1.63 % at 96 h (t 2.30), about 8 times the trade cost, so the 48 h holding cuts the reversal short.
- F4: Inside the thin regime the reversal holds only on the thinnest weekends. By weekend-to-weekday log volume-ratio quartile, the 48 h reversal is +0.57 % on the thinnest quartile (mean -1.20) and -0.40 %, -0.14 % and -1.04 % on the other three.
- F5: The book's 3336 trades lose -0.36 % gross and -0.46 % net on average. Shorts carry the loss: 1797 shorts lose -0.80 % gross while 1539 longs gain +0.14 %. Trades at the capped forecast of 20 lose -0.65 % gross, because the standardised, capped forecast does not separate the large moves that reverse from the rest.
