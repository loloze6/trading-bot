---
brief: 013_anchoring-to-recent-high
source-idea: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound
line: 7.d not profitable
backtest: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's fall on a day, measured against its own volatility over the previous 20 days, is followed by a rise over the next 1 day, only while its 20-day volatility is high relative to its 60-day volatility; the larger the volatility-scaled fall and the higher that volatility ratio, the larger the next day's rise.
Consequence: A trader buys the one-day rebound after sharp falls in a market whose volatility has just expanded, and stays out of rebounds in a calm market, where they lose and only pay fees.
Why:
- F3: The rebound appears only when volatility has expanded: in the lowest tercile of 20-day against 60-day volatility, active bars have excess returns of -0.00143 (t -1.19, n 1303) when the coin fell over 60 days and -0.00171 (t -0.74, n 603) when it rose, against +0.00518 (t 3.35, n 1088) and +0.00554 (t 2.87, n 818) in the highest tercile.
- F1: Fees take 0.000349 of the 0.000804 gross gain per coin per bar, about 43%, at a turnover of 0.33 of the book per bar; the 7100 trades last 1.8 days on average and lose 0.34% before fees and 0.44% after, so the book's mean daily return is 0.000446, below the 0.0005 bar and below holding's 0.00118.
- F5: Of the 0.000804 gross gain per bar, 0.000261 comes from the coins' own rise and the rest from timing, so cutting the bars that time badly (F2, F3) acts directly on the mean return, and on the fees that pull it below 0.0005.
