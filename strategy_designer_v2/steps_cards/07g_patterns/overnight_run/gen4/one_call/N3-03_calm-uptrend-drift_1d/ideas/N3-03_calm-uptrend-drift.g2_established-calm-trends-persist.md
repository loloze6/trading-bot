---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-03_calm-uptrend-drift
line: 7.g patterns
backtest: N3-03_calm-uptrend-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Once a coin's calm-uptrend long has stayed on for more than a week, the move keeps extending, so the days after that point drift up more than the first days after the signal turns on.
Consequence: Expect the first days of a calm-uptrend long to be lossy, and judge the long by its later days rather than by its entry.
Why:
- F3: The book's profit comes from trades that last. 534 trades closed within 1.5 days average -2.14% net with 21% winners, and 559 trades of 1.5 to 3.5 days average -1.39%. Trades longer than 7.5 days average +2.93% (n 392) and those longer than 15 days +10.39% (n 291, 72% winners). Entry forecast size barely matters: quartile means are 0.86%, 0.68%, 0.81% and 1.26%.
- F7: The book's result rests on its tails. Its top 5% of in-position days sum to +38.8 and its bottom 5% to -31.7, against a total of +10.8 over 6,484 in-position days. The 1% daily quantiles are -13.0% and +15.0%.
