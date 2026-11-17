---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and a coin that fell over the weekend rises over those 2 days. In both cases the larger the weekend move relative to the coin's usual daily move, the larger the move back.
Consequence: The weekend move should be faded on both sides and held through Tuesday, which roughly doubles the usable reversal per fee paid compared with a Monday-only short.
Why:
- F1: The book's edge is too small to survive its fees and its idle time. It is flat on Monday to Saturday and holds a short only from the Sunday close to the Monday close, with a mean absolute position of 0.43 on the 1,290 active Sundays. The gain per active Sunday is 0.000776 (t 1.01, 1,284 cases), and the fee on the same Sundays averages 0.000451. The book's mean daily return ends at -3.5e-06 against the 0.0005 required.
- F2: The weekend reversal itself is real. After an up Sunday, Monday returns -0.0046 and the Monday-Tuesday pair -0.0076. After a weekday up-day, the next day returns +0.0005 (t 0.87, 6,117 cases) and the next two days +0.0037. On active Sundays Monday returns -0.0044 (t -2.99) and Tuesday -0.0037 (t -2.78). Holding only Monday therefore leaves half of the fall unused.
- F4: The fall side, which the book never trades, reverses with a clear grading. Sundays in the lowest z sextile (mean z -1.63) are followed by Monday +0.0136 and Wednesday +0.0089. The next sextiles (z -0.58 and -0.13) are followed by Monday +0.0041 and +0.0005, while the average day returns +0.0012.
- F5: Trading both sides makes the effect hold across windows. A vol-scaled position opposite to the Sunday z, held Monday and Tuesday, earns 0.000264 per Sunday (t 2.65, 2,051 cases) and 0.000235 on Monday alone (t 2.83). The short-only version earns t 1.46 over two days, and the book's actual Monday short earns t 0.37. The two-sided version is positive in 62.5% of windows with a worst window mean of -0.0006. The actual book is positive in 37.5% of windows with a worst of -0.0042. By coin it is positive in 5 of 6 coins, strongest in XMR (t 2.56).
