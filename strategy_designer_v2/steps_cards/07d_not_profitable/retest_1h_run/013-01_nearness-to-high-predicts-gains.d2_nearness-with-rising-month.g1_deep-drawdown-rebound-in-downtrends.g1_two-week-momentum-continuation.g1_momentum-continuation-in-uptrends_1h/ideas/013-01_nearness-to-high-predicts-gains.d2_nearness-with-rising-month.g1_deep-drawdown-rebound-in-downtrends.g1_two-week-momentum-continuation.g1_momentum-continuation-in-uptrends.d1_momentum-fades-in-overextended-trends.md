---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Among coins whose 60-day return is positive, the larger a coin's 14-day rise, the higher its return over the next 7 days, only while the 60-day rise is moderate. The further the coin's 60-day return already stands above its usual 60-day gains, the smaller and less reliable that 7-day follow-through becomes.
Consequence: A trader would scale momentum longs by the two-week rise in a rising two-month trend but cut them as the two-month rise becomes extreme, where continuation fades and the deepest falls start.
Why:
- F1: The book fails on Calmar (0.737). Its yearly return is 0.192 and its deepest fall is -26.1%, which ran 225 days from w8 to w10 while the coins fell 36.9%. The worst 30 days alone sum to -1.42 against 1.61 for all days, and on every one of those 30 days the coins fell (mean coin -7.8%).
- F2: Gain is graded by the coin's 60-day return when the book is active, and it collapses at the top. Hourly gain is 0.61, 1.17 and 1.62 bp through the 2nd to 4th quintiles of the 60-day return, then 0.34 bp in the top quintile (60-day return above about +49%), which also has the largest spread (70.7 bp). On the 7-day grid, the forward return in that top quintile is 0.4% against 4.2% in the middle quintile (about 130 cases each).
- F3: Removing the position only when the 60-day return is in its top fifth of active bars has these effects, before fees:
- F4: Other cuts do not repair the falls. Removing the highest 7-day/60-day volatility ratio drops Calmar to 0.90 and removing the highest 7-day volatility gives 1.31; dropping the bars after the weakest 3-day returns gives 1.22. That top-ratio fifth is where the hourly gain is largest (2.27 bp).
