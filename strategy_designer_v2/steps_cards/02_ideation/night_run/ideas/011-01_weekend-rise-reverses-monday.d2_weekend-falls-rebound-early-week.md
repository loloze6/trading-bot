---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days, and the larger the weekend fall relative to its usual daily move, the larger the rise.
Consequence: Sharp weekend sell-offs are a reason to buy into Monday rather than to sell.
Why:
- F4: The fall side, which the book never trades, reverses with a clear grading. Sundays in the lowest z sextile (mean z -1.63) are followed by Monday +0.0136 and Wednesday +0.0089. The next sextiles (z -0.58 and -0.13) are followed by Monday +0.0041 and +0.0005, while the average day returns +0.0012.
- F5: Trading both sides makes the effect hold across windows. A vol-scaled position opposite to the Sunday z, held Monday and Tuesday, earns 0.000264 per Sunday (t 2.65, 2,051 cases) and 0.000235 on Monday alone (t 2.83). The short-only version earns t 1.46 over two days, and the book's actual Monday short earns t 0.37. The two-sided version is positive in 62.5% of windows with a worst window mean of -0.0006. The actual book is positive in 37.5% of windows with a worst of -0.0042. By coin it is positive in 5 of 6 coins, strongest in XMR (t 2.56).
