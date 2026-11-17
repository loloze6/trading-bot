---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: Among coins whose 60-day return is positive, the larger a coin's 14-day rise, the higher its return over the next 7 days.
Consequence: A trader would add to long positions in proportion to the two-week rise while the coin's two-month trend is up, rather than taking the short side of the same signal.
Why:
- F1: The tested slope holds wherever the 7-day grid starts: in the trending regime the t of the 14-day return, controlled for the 1-day return, stays positive at all seven grid offsets (2.75, 2.07, 3.37, 3.58, 3.06, 4.61, 2.01; about 1,000 to 1,085 cases each), and the demeaned 7-day return rises across the trending 14-day-return quintiles from -0.0223 (t -2.60) to +0.0222 (t 1.68), 217 cases each.
- F2: Outside the trend the same signal does nothing: in the non-trending regime the 14-day return's correlation with the demeaned 7-day return is 0.030 (p 0.33, n 1,070), against 0.102 (p 0.0008, n 1,085) in the trending regime.
- F6: The book's edge is spread across coins: its mean daily return is above zero in 5 of 6 coins (0.00042 to 0.00139), with LTC the exception (-0.00007), and it loses less than holding the coins in the down years 2018 (-0.00035 against -0.00347) and 2022 (-0.00047 against -0.00180).
