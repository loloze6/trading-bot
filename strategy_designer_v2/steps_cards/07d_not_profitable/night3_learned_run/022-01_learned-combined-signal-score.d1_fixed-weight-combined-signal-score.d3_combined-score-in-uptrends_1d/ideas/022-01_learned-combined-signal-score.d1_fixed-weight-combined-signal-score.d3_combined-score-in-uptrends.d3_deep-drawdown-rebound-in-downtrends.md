---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 28-day return is down, its return over the next 5 days is higher the further its close lies below its 90-day high.
Consequence: In a falling month, a trader would lean long a coin in proportion to how deep it sits below its 90-day high, rather than short it.
Why:
- F8: While the 28-day return is down, distance below the 90-day high predicts the next 5 days: correlation -0.094, t -2.58, 751 cases. The further a falling coin is below its 90-day high, the higher its next 5-day return.
- F5: The size per case is -0.74 % in total and -0.65 % unusual, against a 0.19 % round trip: -3.8 and -3.4 times the cost. No holding period or sizing can turn this into a gain. The cause is the sign of the bets, not the cost.
