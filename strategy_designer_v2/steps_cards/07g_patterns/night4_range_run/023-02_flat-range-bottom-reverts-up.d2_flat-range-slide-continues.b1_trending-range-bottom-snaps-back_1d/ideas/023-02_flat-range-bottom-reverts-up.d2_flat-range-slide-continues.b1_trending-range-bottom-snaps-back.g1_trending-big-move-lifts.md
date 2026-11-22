---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 10-day move in either direction, the more it rises over the next 5 days.
Consequence: In a trending coin, a large 10-day move up or down is a reason to lean long for the following days, and to refuse shorts.
Why:
- F1: In trending coins (30-day net move at least half the 30-day high-low range), the size of the 10-day move in either direction predicts a higher 5-day return. Pooled over the coins, the slope of the 5-day excess return (z) on |10-day return z| is +0.187 with t 5.03 over 1113 non-overlapping cases. It is positive in all six coins, with t 4.22 in ZEC, 2.38 in ETH and 2.31 in XRP. Both tails rise: the bottom quintile of the 10-day return gives +1.71 % excess (t 2.01, 234 cases) and the top quintile +1.46 % (t 1.90, 301 cases), while the middle quintiles are near zero or negative.
- F5: The tested idea's graded slope (t 3.79) rides on the coins' drift, not on a reversion. Its unusual move is -0.37 % per case (-0.030 of a usual 10.60 % move, 751 cases), and the total move of +0.23 % is only 1.2 times the 0.19 % cost of a trade.
