---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 8 days, only once its closes over the following 2 days stay above that level, and the further above the level those closes stay, the larger the rise.
Consequence: A trader would buy a break of a repeatedly held level only after it has held for two days, and would refuse breaks that slip back under the level, which carry the deepest losses.
Why:
- F3: A break's fate shows on the next day. Among the 895 entries with 10 days of room, the 775 whose next close stays above the broken level gain +1.79 % over 5 days (t 4.25). The 120 that close back below it lose -4.55 % (t -4.79). Measured from the second day's close, breaks still above the level after two days rise +1.38 % over the next 8 days (t 2.40, 680 cases), while those that fell back gain -0.06 % (t -0.07, 215 cases).
- F4: Breaks that fell back by day 2 still gain +0.43 % from day 2 to day 5 (t 0.75), about the same as the breaks that held (+0.36 %, t 1.08). The fall-back's loss lies in the fall-back itself, not in a continued decline after it.
- F7: All entries average +0.73 % over 5 days (t 1.96, 974 entries), but they pass on average through a low of -4.0 % on the way, and 53 % of them end below their entry. The touch-count-times-margin value does not grade the result: its quintiles give +1.1 %, +0.3 %, +1.0 %, -0.5 % and +1.7 %.
- F1: The book's deepest fall is 50.0 %, and its Calmar of 0.49 fails the 0.75 bar. The fall runs 276 days from w1 to w4, with the book's daily returns summing to -0.63 while the coins' sum to -0.71, so the book rode the coins' shared decline almost in full.
