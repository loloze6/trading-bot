---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its long moving average, the nearer its close sits to the top of its recent range and the stronger its recent rise, the larger its return over the following days to two weeks. The effect fades by about a month.
Consequence: Hold momentum longs inside an uptrend for days to a couple of weeks, not a month, and size them by how close price is to its recent high.
Why:
- F5: The tested book loses to its own churn. Its gross gain per day is positive in BTC, ETH and XRP (+0.09% to +0.11%), but fees per day are larger in every coin (0.155% to 0.250%). Trades held 3 hours or less lose 0.54% to 0.78% before fees (about 30,700 trades), while trades held over 14 hours gain 3.47% (12,610 trades).
- F6: The tested forecast does better over two weeks than over a day. In the trending regime, the top half of positive forecasts is followed by +4.7% excess over the next 336 hours (t 1.9, n 181), but by -0.15% over the next 24 hours (t -1.6, n 2898). This matches the plan's slope t of 2.18 alongside a losing hourly book.
