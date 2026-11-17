---
brief: 013_anchoring-to-recent-high
source-idea: 013-04_heavy-volume-below-high-breakout
line: 7.d not profitable
backtest: 013-04_heavy-volume-below-high-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's close is to its highest high of the past 120 days, the larger its return over the next 30 days.
Consequence: A trader would hold coins near their recent high, in proportion to how near they are, which keeps the book in the market far more often than breakout days alone.
Why:
- F5: Closeness to the high is graded even without a break. On the 30-day grid, the 30-day return rises across quintiles of distance from the in-window running high: 0.005, 0.021, 0.033, 0.051, then 0.063 for the nearest. The Spearman rho is 0.096 (p 0.06, n 388).
- F1: The book is almost never in the market, and this is why it fails on size, trades and Calmar. It is long on only 1.4% of bars, from 0.7% for XRP to 2.4% for ETH. Its 165 trades last a mean of 1.52 days and a median of 1 day. As a result it trades 0.0095 per bar, earns a mean daily return of 5.9e-05 against the coins' 0.00129, and has a daily return SD of 0.0052 against holding's 0.048.
- F3: The extra rise continues for weeks after the break. On the non-overlapping 30-day grid, bars 1 to 10 days after a break return 0.082 (14 cases) and bars 10 to 30 days after return 0.068 (31 cases). Bars in windows with no break return 0.028 (457 cases). The 30 days after breaks cover 12.3% of bars against the book's 1.4%.
