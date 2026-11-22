---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The busier a coin's five weekdays were compared with its volume over the past 30 days, the larger the share of its Saturday-Sunday move that is reversed over the next 2 days (Monday and Tuesday).
Consequence: A trader would lean against a weekend move at Sunday's close more strongly after an unusually busy trading week, and less after a quiet one.
Why:
- F5: The thinness effect comes from busy weekdays, not from quiet weekends. Measured against 30-day volume, weekday volume in its top quartile gives a reversal of +0.103 (t 1.96, n 453) against -0.075, -0.078 and -0.029 in the other quartiles. The weekend's own volume against 30 days shows no order (+0.023, -0.096, +0.053, -0.060).
- F2: How thin the weekend was sets the outcome on a graded scale. Thinness is the five weekdays' mean volume over the weekend's mean volume. In its top quartile the weekend move reverses over the next 48 h: weekend rises reverse by +0.219 of a usual move (t 3.55, n 234, total +1.16 %) and weekend falls by +0.060 (t 0.96, n 219, total +0.61 %). In its bottom quartile the move continues instead: falls by -0.200 (t -2.18, n 187, total -1.15 %) and rises by -0.131 (t -1.73, n 267, total -1.21 %).
- F6: The effect belongs to the weekend. The same thinness measure read at Wednesday's close gives 48 h reversals of only -0.043 to +0.032 across its quartiles (all |t| < 1.3). The mean thinness ratio is 1.95 on Sunday against 1.00 on Wednesday.
