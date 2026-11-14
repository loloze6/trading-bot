---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily returns are higher while it closes above its long moving average than while it closes below it. The book's edge is mainly being exposed in that up regime and absent in sustained declines.
Consequence: Use the long-average regime as an exposure switch for owning the coin, and expect it to pay mainly by sitting out bear years, not by timing within trends.
Why:
- F1: The book's gain is mostly the market's own rise taken part-time. Its daily beta to the coin is 0.18 (r² 0.25), it is in the market 44% of bars at a mean allocation of 0.19, and the alpha left is only 3.5 bps/day. It earned in the up years 2020 (gain 20.1 bps/bar on a 42.3 bps coin drift, 63% in market) and 2024 (12.5 bps on 24.4). It stayed out of 2022 (8% in market, coin −18.0 bps) and lost only 1.7 bps there.
- F8: In-market bars are followed by a mean next-bar return of 19.7 bps against 5.7 bps for out-of-market bars (Welch t 1.85).
- F6: It is not one coin's book, but three coins carry it. BTC, ETH and XRP earn about 10 bps/day (book Sharpe 1.19, 1.12 and 0.89), while LTC (−0.05 bps) and XMR (0.7 bps) earn nothing. The lowest leave-one-coin-out portfolio Sharpe is 0.77, with BTC left out.
