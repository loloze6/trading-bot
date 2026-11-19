---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal
line: 7.d not profitable
backtest: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 1 day runs against its own 1-day return measured once a day at the same hour, and the larger that day's move relative to the coin's recent volatility, the larger the move back over the following day.
Consequence: The reversal is a day-to-day effect, so a position reset once a day captures it, while hour-to-hour changes in the rolling daily return carry no gain and only cost fees.
Why:
- F1: The book makes almost nothing before fees and loses to fees. Its gross gain is 0.000073 a day, while its fees cost 0.00284 a day. Turnover is 2.63 times the book a day, trades last a median of 5 hours, and there are 195,067 trades averaging -0.31% before fees and -0.41% after. So the book's mean daily return is -0.00274 (sd 0.0252, n 17381), against +0.00119 for holding.
- F2: The reversal is real only at the one-day horizon, and the book rebalances every hour. On non-overlapping grids, forecast/10 times the forward return earns 0.000026 per hour at 1 bar, 0.000014 per hour at 4 bars and 0.000070 per hour at 24 bars (0.00167 per case). Meanwhile the forecast's autocorrelation is 0.94 at 1 hour, 0.70 at 6 hours and -0.05 at 24 hours. The book therefore trades the hour-to-hour drift of a rolling 24-hour return that carries almost no hourly gain.
