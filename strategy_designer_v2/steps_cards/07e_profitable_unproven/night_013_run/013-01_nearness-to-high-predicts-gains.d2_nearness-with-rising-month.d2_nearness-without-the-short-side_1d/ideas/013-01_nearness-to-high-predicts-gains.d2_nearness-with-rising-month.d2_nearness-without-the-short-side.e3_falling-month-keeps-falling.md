---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side
line: 7.e profitable but not proven
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The more negative a coin's 30-day return, the lower its return over the next 3 days.
Consequence: A coin with a falling month is a reason to refuse a long trade over the next few days, more firmly the deeper the fall.
Why:
- F8: Part of the book's edge is standing aside from falling coins. Bars with a 30-day return at or below 0 have a 3-bar excess return of -0.00322 (t -2.23, n 2768) and a 7-bar one of -0.00702 (t -1.96, n 1179).
- F4: The edge is strongest at a shorter horizon than the plan's 7 bars. The Welch t of active bars minus flat bars is 2.91 at 3 bars (2798 active cases, active mean excess 0.00318, t 1.92), 2.58 at 7 bars and 1.83 at 1 bar. It fades to 0.98 at 14 bars and 0.70 at 30 bars.
