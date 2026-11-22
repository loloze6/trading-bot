---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday rise is partly reversed over the next four days, only while its preceding five weekdays fell and its weekend volume is lower than its mean volume over those weekdays; the larger the weekend rise and the lower the weekend volume against the weekdays, the larger the share reversed.
Consequence: A trader shorts a thin weekend rise only when it is a bounce inside a falling week, holds the short through Thursday, and refuses it after a rising week.
Why:
- F3: What happened on the weekdays before decides the sign, and the effect is larger over four days than over two: after a weekend rise that followed a weekday rise, the coin kept rising (the short's total is −0.65 % over 48 h, t −1.97, and −1.00 % over 96 h, t −2.20, 593 cases); after a weekend rise that followed a weekday fall, the short gained +0.11 % over 48 h (t 0.43) and +0.47 % over 96 h (t 1.24, 616 cases).
- F2: The book pays the cost about twice per weekend and loses on most trades: 1,796 short trades on about 952 active weekends (459 lasted under 1.5 h and 348 lasted 1.5–24 h), a mean of 42.6 allocation changes inside each 48-hour hold, a gross mean of −0.93 % and a net mean of −1.03 % per trade, and 26 % winners.
- F1: The move per case is too small to pay for a trade, and the coin's own rise works against the short: over the 48 hours after the 717 active weekends the short's total move is −0.18 % (t −0.75), and the step-5 size is +0.03 % total and +0.29 % unusual, against a 0.19 % cost per trade.
