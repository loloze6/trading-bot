---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-03_deep-month-loss-rebound
line: 7.g patterns
backtest: N2-03_deep-month-loss-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After an unusually large daily fall, the coin's excess return is concentrated in the first following day, and the gain does not continue over the next four days.
Consequence: Rebound longs taken after sharp falls should be closed after about a day rather than held for weeks, because the long holds are where the book lost.
Why:
- F3: The rebound is spent within a day. In spaced events, the return from day 1 to day 5 after a down day of one standard deviation or more is not distinguishable from zero in any volatility tercile: 0.0034 (t=0.78), 0.0031 (t=0.69) and 0.0096 (t=1.55), with n of about 376 each.
- F6: The book earns on short holds and loses on long ones. Trades held up to 1.5 days average +2.20% net (n=707, 74% wins) and trades held 1.5 to 5 days average +1.30% (n=1088). Trades held over 15 days average -6.48% (n=743, 29% wins) and sum to -4811% of net P&L, against +2794% for all shorter trades.
