---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.d not profitable
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily fall on a volume burst at least 2 times the 20-day median, the shorter the bar's lower wick relative to its range, the larger the price rise over the next 1 day.
Consequence: The day after a high-volume selloff, a trader would buy when the close sits near the low and stand aside when a long wick shows the selling was already absorbed inside the bar.
Why:
- F1: The long lower wick that the tested situation requires marks the wrong falls. Sharp falls (one-day return at or below -2 of its 20-day standard deviation) with a wick of at least 0.3 of the range were followed by a next-day excess return of -1.46% (t -2.36, n=86) and a 3-day excess of -0.83%. The same falls without the wick were followed by +1.12% next day (t 3.33, n=324). The flush bars the book traded were followed by a next-day excess of -0.71% (t -1.17, n=89).
- F2: The book loses because of the bar after the flush. Its 88 trades were held about 1.03 days on average and returned -0.78% before fees and -0.88% after fees. That puts the mean daily return at -4.5e-05, Sharpe at -0.28 and Calmar at -0.09. The position size was not the problem: the mean allocation when held was 1.08.
- F5: The wick is graded against the rebound. Among volume-burst sharp falls, the next-day return by wick tercile was +1.67% (t 1.85), +0.51% and -0.37%. Among falls of at least 1.5 standard deviations, the next-day excess by wick tercile was +0.75%, +0.63% and -0.07%.
