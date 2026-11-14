---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin is in an uptrend, the next day's return is larger the further its recent returns stand above their own usual size.
Consequence: A trader can scale a long position with how unusually strong the coin's current up-move is relative to its own history.
Why:
- F1: The book's gain is mostly timing and not the market's rise: of the 0.000804 mean daily gain before fees, the coin's drift × allocation explains 0.000252 and timing explains 0.000553 (t 3.64). The book is in the market on only 29–38% of days per coin. The coins' next-day return is 0.002937 on in-market days against 0.000311 on flat days (Welch t 3.21).
- F4: Within active days, the next-day coin return grows with signal size. By forecast quartile (mean forecast 4.0, 9.6, 13.9, 19.0), the next-day return is 0.00181, 0.00276, 0.00405 and 0.00458, and the position gain is 0.00049, 0.00129, 0.00314 and 0.00486.
